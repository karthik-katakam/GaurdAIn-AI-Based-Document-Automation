import {React, useState, useEffect} from "react";
import { Document, Page, pdfjs } from "react-pdf";
import { useLocation } from "react-router-dom";
import Header from "../components/Header";
import "../FileAnalysis.css";
import DownloadPDF from "../components/DownloadPDF";

// Correctly set workerSrc using a CDN
pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.js`;
function FileAnalysis() {
  const location = useLocation();
  const fileUrl = location.state?.fileUrl; // Retrieve fileUrl correctly

  if (!fileUrl) {
    return <p>No file uploaded. Please go back and upload a PDF file.</p>;
  }

  return (
    <>
      <Header />
      <div className="file-analysis-container">
        {/* PDF Viewer */}
        <div className="pdf-preview">
          <Document file={fileUrl} onLoadError={(error) => console.error("Error loading PDF: ", error)}>
            <Page pageNumber={1} />
          </Document>
        </div>

        {/* Fraud Analysis Section */}
        <div className="fraud-analysis">
          <h3>Fraud Score: <span className="score-highlight">7/10</span></h3>
          <h4>Fraud Analysis/Comparison</h4>
          <ul>
            <li>🔴 Ending cash balance for 2024 is oddly significantly higher than in 2023, signifying an unusual spike or potential misrepresentation.</li>
            <li>🔴 No proper amount description for the sale of property income, signifying potential false amounts.</li>
            <li>🔴 Total income received is less than ending cash balance.</li>
            <li>🟠 Gas & EZ Pass are listed as disbursements, but no vehicle is listed as an asset. Possible inconsistency.</li>
            <li>🟠 Additional disbursements (Health Insurance & Housing Rent) are missing in 2024 compared to 2023.</li>
          </ul>
          <DownloadPDF />
        </div>

        {/* Extracted Text Section */}
        <div className="extracted-text">
          <h3>Extracted Text</h3>
          <p><strong>Guardian Name:</strong> Sam Jones</p>
          <p><strong>Incapacitated Person's Name:</strong> John Smith</p>
          <p><strong>Beginning Cash Balance:</strong> 140,971.66</p>
          <p><strong>Income:</strong> $810,169.00</p>
          <p><strong>Disbursements:</strong> $106,146.58</p>
          <p><strong>Ending Cash Balance:</strong> $844,994.08</p>
        </div>
      </div>
    </>
  );
}

export default FileAnalysis;