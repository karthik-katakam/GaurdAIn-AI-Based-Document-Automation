import {React, useEffect, useState} from 'react';
import { Link, redirect } from 'react-router-dom';
import Header from '../components/Header';
import Footer from "../components/Footer";
import { pdfjs } from 'react-pdf';
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import axios from 'axios';
import "../styles.css";


pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

function CaseListings() {
  const [cases, setCases] = useState([]);
  const [theCase, setTheCase] = useState('');
  const [theStatus, setStatus] = useState('');
  const [userSearchData, setUserSearchData] = useState('');




  const getAllCases=()=>{

    axios.get("http://localhost:5000/case-detail").then((res)=>{
      setCases(res.data)
      setUserSearchData(res.data)

    })
  }

  const handleSearch = () =>{

     if(theStatus=="All")
      {
        console.log(theStatus)
        axios.get("http://localhost:5000/case-detail").then((res)=>{
          setCases(res.data)
        }
         )}
  
   else if(theCase){
    const newData = userSearchData.filter(x=> x.casename.toLowerCase().includes(theCase.toLowerCase()))
    setCases(newData)
    console.log(newData)
    }

   else if(theStatus){
      const newData = userSearchData.filter(y=> y.status.toLowerCase().includes(theStatus.toLowerCase()))
    
    setCases(newData)
    console.log(newData)
    console.log(theStatus)
    alert('alert')
    }
   
      else 
        {
          console.log(theStatus)
          axios.get("http://localhost:5000/case-detail").then((res)=>{
            setCases(res.data)
          }
           )}
  }
    
 

  useEffect(()=>{
          getAllCases()
          document.title="Case Listings";
        }, []);
  return (
    <>
    <Header />
   <div className="case-listings">
             {/* This data below will maybe need to be pulled from database? */}
             <h2>Case Listings</h2>
             <table style={{backgroundColor:"white" }} >
              
               <thead>

             
                 <tr>
                   <th>Case Name</th>
                   <th>Date</th>
                   <th>Docket #</th>
                   <th>Case Description</th>
                   <th>Case Type</th>
                   <th>Status</th>
                 </tr>
               </thead>
               <tbody>
                  
                 {cases && cases.map(cases=>{
                  return(<tr>
                   <td><Link to={"/case-detail/" + cases.id} className="case-link">{cases.casename}</Link></td>
                   <td>{cases.date}</td>
                   <td>{cases.docketnum}</td>
                   <td>{cases.description}</td>
                   <td>{cases.casetype}</td>
                   <td><span className="status ongoing">
                    
                    {cases.status==="Resolved" ? "🟢 Resolved"  : cases.status==="Open"? "⚪ Open" : cases.status==="Pending"? "🟡 Pending": cases.status==="Closed" ? "🟢 Closed": "🔴 Emergency"  } 
                    </span></td>
                  </tr> )})}
               </tbody>
               
             </table>
           </div>

            <div class="filterSearch">
           <input type = "text"  class = "filter" placeholder="Filter Search" onChange={(e)=> setTheCase(e.target.value)}/>
           <select onChange= {(e) => setStatus(e.target.value)}>
                    <option value='Pending'>Pending</option>
                    <option value='Open'>Open</option>
                    <option value='Closed'>Closed</option>
                    <option value='All'>All</option>



           </select>
           <button onClick={()=> handleSearch()}>Search</button>

           </div>

         

    <Footer/>
    </>
    
  );

}

export default CaseListings;