import {React, useState, useEffect} from 'react';
import { useParams } from 'react-router-dom';
import Header from '../components/Header';
import Footer from "../components/Footer";
import axios from 'axios';

function CaseDetail() {
  let { id } = useParams();
  const [cases, setCases] = useState([]);

  const getCaseDetails=()=>{

    axios.get(`http://localhost:5000/case-detail/${id}`).then((res)=>{
      setCases(res.data)

    })
  }

  useEffect(()=>{
     getCaseDetails()
            document.title="Case Listings";
          }, []);
  
  return (
    <>
    <Header />

    {/*All this data will be grabbed by database */}
    <h1> <center>Case Details</center></h1>
    <div className="container">
      <p><b>Details for Case ID:</b> {id}</p>
      <p><b>Status: </b>{cases.status}</p>
      <p><b>Parties:</b> {cases.parties}</p>
      <p><b>Plaintiff:</b> {cases.plaintiff}</p>
      <p><b>Alleged Incapacitated Person (AIP):</b>  {cases.aip}</p>
      <p><b>Case Type:</b> {cases.casetype}</p>
      <p><b>Is the Plaintiff the proposed guardian(s):</b> {cases.plaintiff}</p>
      <p><b>Are any other person(s) proposed guardian(s):</b> {cases.otherguardians}</p>
      <p><b>All person(s) proposed as guardian(s): </b> {cases.allguardians}</p>
      <p><b>Does any party need an interpreter?</b> {cases.interpreterneeded}</p>
      <p><b>If yes, for whom and for what language?</b> {cases.interpreterpersonlanguage}</p>
      <p><b>Does any party need an accommodation for a disability?</b> {cases.disabilityaccommodation}</p>
      <p><b>If yes, please identify the party and requested accommodation</b> {cases.accommodationparty}</p>
      <p><b>I certify that I have completed this form to the best of my knowledge and ability, 
        and will supplement this form as may be necessary should additional information become available. I further certify that, except as required on this 
        page, confidential personal identifiers have been redacted from documents now submitted to the court, and will be redacted from all documents submitted in 
        the future in accordance with Rule 1:38-7(b).</b></p>
      <p><b>Date:</b> {cases.date}</p>
      <p><b>Attorney/Plaintiff Signature:</b> {cases.signature}</p>

    </div>
    <Footer/>
    </>
  );
}

export default CaseDetail;