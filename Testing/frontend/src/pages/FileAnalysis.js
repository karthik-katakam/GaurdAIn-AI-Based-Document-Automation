import React, { useEffect } from "react";
import Header from "../components/Header";
import "../FileAnalysis.css";

export default function FileAnalysis() {
  // replace this with the URL your backend actually serves
  const fileUrl = "11800_grdnshp_ez_accting_validated.pdf";
  // if you copied it into public/annotated, you could use:
  // const fileUrl = "/annotated/11800_grdnshp_ez_accting_validated.pdf";

  useEffect(() => {
    console.log("🔍 Iframe loading PDF from:", fileUrl);
  }, [fileUrl]);

  return (
    <>
      <Header />
      <div className="file-analysis-container">
        <p style={{ fontSize: "0.9em", color: "#555" }}>
          Loading PDF in an iframe from: <code>{fileUrl}</code>
        </p>
        <iframe
          title="PDF Viewer"
          src={"11800_grdnshp_ez_accting_validated.pdf"}
          width="100%"
          height="800px"
          style={{ border: "none" }}
        />
      </div>
    </>
  );
}
