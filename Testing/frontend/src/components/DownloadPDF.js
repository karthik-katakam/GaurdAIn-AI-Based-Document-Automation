import React from "react";
import { jsPDF } from "jspdf";
import html2canvas from "html2canvas";

const ExportClassDivsPDF = () => {
  const handleDownloadPDF = async () => {
    // Select all elements with the "exportable" class
    const exportableElements = document.querySelectorAll(".fraud-analysis", );

    // Create a temporary container to combine them
    const container = document.createElement("div");
    container.style.padding = "20px";
    container.style.backgroundColor = "#fff";
    container.style.color = "#000";

    exportableElements.forEach((el) => {
      const cloned = el.cloneNode(true);
      cloned.style.marginBottom = "20px";
      container.appendChild(cloned);
    });

    // Append to body temporarily for rendering
    document.body.appendChild(container);

    // Convert to canvas
    const canvas = await html2canvas(container, {
      scale: 3,
      useCORS: true,
    });

    const imgData = canvas.toDataURL("image/png");
    const pdf = new jsPDF("p", "mm", "a4");

    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = pdf.internal.pageSize.getHeight();

    pdf.addImage(imgData, "PNG", 0, 0, 450, pdfHeight);
    pdf.save("fraud-report.pdf");

    // Clean up
    document.body.removeChild(container);
  };

  return (
    <button onClick={handleDownloadPDF} style={{ marginTop: "20px" }} className="download-btn">
      Download Fraud Report
    </button>
  );
};

export default ExportClassDivsPDF;
