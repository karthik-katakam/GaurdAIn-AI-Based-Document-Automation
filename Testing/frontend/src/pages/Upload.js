import React, { useState, useEffect, useRef, useCallback, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header.js";
import Footer from "../components/Footer.js";
import "../Dashboard.css";
import "../Directory.css";
import "../Upload.css";
import {baseStyle, activeStyle, acceptStyle, rejectStyle} from "./upload-styles.js"
import { pdfjs } from "react-pdf";
import { useDropzone } from 'react-dropzone';
import ReCAPTCHA from "react-google-recaptcha";
import ProgressBar from "../components/ProgressBar.js";
import axios from "axios";
// Correctly set workerSrc using a CDN
pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.js`;
function Upload(props) {
  
   useEffect(()=>{
      
          document.title="File Upload";
        }, []);
  const [cases, setCases] = useState([]);
  //setting the state of whether file is selected or not
  const [selectedFile, setSelectedFile] = useState(null);
  //setting progress for progress bar
  const [progress, setProgress] = useState(0);
  // setting state whether file is uploading
  const [isUploading, setIsUploading] = useState(false);
  //let us move between routes (go to other pages)
  const navigate = useNavigate();
  
  const recaptcha = useRef();
  const port = 8000

  //callback function runs when a file is selected & dropped. File is set to the file dropped. Creates a temp url.
  const onDrop = useCallback(acceptedFiles => {
    const file = acceptedFiles[0];
    
    setSelectedFile(Object.assign(file, {
      preview: URL.createObjectURL(file)
      
    }));
    

  }, []);

  const getAllCases=()=>{

    axios.get("http://localhost:5000/case-detail").then((res)=>{
      setCases(res.data)

    })
  }
  
  //begin the upload process. 
  const startUpload = () => {
    console.log("hi")
    setProgress(0);
    setIsUploading(true); //starts uploading
    console.log(isUploading)
  }


  //After the file upload component renders, run the startUpload function as after effect
  useEffect(()=>{

    if(selectedFile)
    {
      startUpload()
    }
  }, selectedFile);

  
  //After file upload component renders, if file upload is not 100%, keep updating progress by +10 until 100. If 100, clear and stop interval (loop) and stop 
  useEffect(()=>{
    if(isUploading && progress < 100)
    {
      const interval = setInterval(() => {
        setProgress((prevProgress)=>
          {
            if(prevProgress>=100) {
              clearInterval(interval);
              setIsUploading(false);
              return 100;
            }
            return prevProgress + 10
          });

      }, 1000);
      return ()=> clearInterval(interval);
    }
  }, [isUploading, progress]);

    useEffect(()=>{
            getAllCases()
          }, []);

  // Properties of dropzone. Run these actions(make these props active) based on drop activity status. Also on drop, accept PDF
  const {getRootProps, getInputProps, isDragActive, isDragAccept, isDragReject}= useDropzone({onDrop, accept:"application/pdf"});

  const StyleComponent = ({isDragActive, isDragAccept, isDragReject})=>{
    //useMemo - remember the output after a render and dont re-render unless any dependency changes 
    //implement style based on whether drag is active, accepted, or rejected
  const style = useMemo(() => ({
    ...baseStyle,
    ...(isDragActive ? activeStyle: {}), 
    ...(isDragAccept ? acceptStyle: {}), 
    ...(isDragReject ? rejectStyle: {}), 
  }), [
    isDragActive,
    isDragReject,
    isDragAccept
  ]);

  };

 

  // // clean up
  // useEffect(() => {
  //   if (selectedFile) {
  //     return () => URL.revokeObjectURL(selectedFile.preview);
  //   }
  // }, [selectedFile]);
  
//when file is uploaded, if file exists and is pdf, set selected file to the file uploaded. Else, ask to uplaod a valid file
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && file.type === "application/pdf") {
      setSelectedFile(file);
    } else {
      alert("Please upload a valid PDF file.");
    }
  };
//Show progress bar percentage (and increasing) if percentage is <100. Once 100+, state that its complete.
  const theProgressBar = () =>(
    <div id="progress_bar" className="progress-bar">
      {progress < 100 ? (
        <>
          <ProgressBar
            progress={progress}
            color="green"
            height="14px"
            />
            
            <p>Uploading: {progress}%</p>
        </>
      ): (<p>Upload Complete!</p>)}
    </div>
  );
  //generate url for the file uploaded. Then open that url to a tab when clicking view
  const handleViewVerify = () => {
    if (selectedFile) {
      window.open(URL.createObjectURL(selectedFile), "_blank");
    } else {
      alert("Please select a PDF file to preview.");
    }
  };

  //when submit for scan button clicked
  const handleSubmitForScan = async () => {
    const captchaValue = recaptcha.current.getValue();
  
    if (!selectedFile) {
      alert("Please upload a file before submitting.");
      return;
    }
  
    if (!captchaValue) {
      alert("Please confirm you are not a robot with reCAPTCHA.");
      return;
    }
  
    try {
      // Step 1: Verify reCAPTCHA token with backend
      const captchaResp = await fetch(`http://localhost:${port}/verify-captcha`, {
        method: "POST",
        body: JSON.stringify({ captchaValue }),
        headers: {
          "Content-Type": "application/json",
        },
      });
  
      const captchaData = await captchaResp.json();
  
      if (!captchaData.success) {
        alert("reCAPTCHA failed. Please try again.");
        return;
      }
  
      // Step 2: Upload file to backend
      const formData = new FormData();
      formData.append("file", selectedFile);
  
      const uploadResp = await fetch(`http://localhost:5001/process_pdf`, {
        method: "POST",
        body: formData,
      });
  
      const uploadData = await uploadResp.json();
  
      if (uploadData && uploadData.pdfUrl && uploadData.data) {
        // Step 3: Navigate to analysis page with data
        navigate("/file-analysis", {
          state: {
            fileUrl: uploadData.pdfUrl,
            extractedData: uploadData.data,
          },
        });
      } else {
        alert("Error: Upload failed or invalid response.");
      }
    } catch (error) {
      console.error("Upload error:", error);
      alert("An error occurred while processing your request.");
    }
  };
  
  return (
    <>

      <Header />
      <div className="upload-container">
        <h1>Upload Documents for Case</h1>
        
        {/* Select Case Dropdown */}
                  <select className="case-dropdown">
                  <option>Select Case</option>
                  {cases && cases.map(cases=>{
                    return(
                  <div>
                  <option>{cases.casename}</option>
                  </div>
                  )})}
                  </select>
      
        {/* File Upload Box */}
        <div className="upload-box">
           {/* Props to enable drag n drop into border */}

          <div className= "upload-border" {...getRootProps({StyleComponent})}>
          <input {...getInputProps()}/>
            <img src="/open folder.svg" alt="Upload Folder" className="folder-icon" />
            <p>Drag & Drop to Upload File</p>
        
            <p>OR</p>
          </div>
          
            <label className="file-upload-button">
              
              <input type="file"  onChange={handleFileChange} accept="application/pdf" hidden     />
              
              Browse Files
            </label>
            {/* Show selected file name and progress bar once file uploaded */}
            {selectedFile && <p className="file-name">Selected: {selectedFile.name} {theProgressBar()}  </p>}
    
  
            
            {/* reCAPTCHA */}
            <div className="recaptcha-placeholder">
              <ReCAPTCHA ref={recaptcha} sitekey={process.env.REACT_APP_SITE_KEY} />
            </div>

            {/* Buttons */}
            <div className="button-group">
              <button onClick={handleViewVerify} className="btn verify-btn">View & Verify</button>
              <button onClick={handleSubmitForScan} className="btn submit-btn">Submit for Scan</button>

            </div>
           
        <p className="upload-info">Upload any documents to the Guardianship Case for analysis</p>

        </div>

      </div>
      <Footer/>

    </>
  );
}

export default Upload;