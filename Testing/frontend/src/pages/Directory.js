import {React, useEffect} from 'react';
import Header from '../components/Header';
import { Link } from 'react-router-dom';
import "../Directory.css";
import Footer from "../components/Footer";

function Directory() {

    useEffect(()=>{
    
        document.title="Directory";
      }, []);
  return (
    <>
      <Header />
      <div className="directory-container" >
        <div className="sidebar" style={{paddingTop:"130px"}}>
          <Link to="/case-listings" className="sidebar-card visible-card">
            <div className="card-content">
              <h2>Case Listings</h2>
              <div className="icon">
                <i className="fas fa-list"> <img src="/list.svg" alt="List" className="folder-icon" /> </i>
              </div>
            </div>
          </Link>
          <Link to="/dashboard" className="sidebar-card grey-card">
            <div className="card-content">
              <h2>Fraud Dashboard</h2>
              <div className="icon">
                <i className="fas fa-chart-line"><img src="/arrow-trending.svg" alt="Dashboard" className="trending-icon" /></i>
              </div>
            </div>
          </Link>
          <Link to="/upload" className="sidebar-card grey-card">
            <div className="card-content">
              <h2>Case File Upload</h2>
              <div className="icon">
                <i className="fas fa-upload"><img src="/open folder.svg" alt="Upload Folder" className="folder-icon" /></i>
              </div>
            </div>
          </Link>
          
        </div>
        <div className="directory-content">
          <h1 style={{paddingBottom: "80px" }}><center>Directory</center></h1>

          <div className="sidebar-card grey-card" >
          <div className="card-content">
          <h2 >Quick Information Links </h2>
          <div style={{ whiteSpace: 'pre-line' }}>
          <ul>          {"\n"}

              <li><a href="#"><b>Frequently asked questions</b></a></li>
              <li><a href="https://github.com/allydrzewo/NJ-Courts"><b>Documentation</b></a></li>
              <li><a href="#"><b>About</b></a></li>
              <li><a href="https://www.njcourts.gov/self-help/guardianship#toc-guardianship-reporting-requirements" ><b>Guardianship Reporting Requirements</b></a></li>
              <li><a href="#"><b>Guardianship Forms</b></a></li>
              <li><a href="https://www.njcourts.gov/self-help/guardianship#toc-concerns-about-a-guardianship"><b>Guardianship Concerns</b></a></li>
              
            </ul>
            </div>
            </div>
          </div>
           
          </div>
        </div>
      <Footer/>
      {/* <div className="footer">
        <div className="footer-section">
          <h3>Product</h3>
          <ul>
            <li><Link to="/caselistings">Case Listings</Link></li>
            <li><Link to="/dashboard">Dashboard</Link></li>
            <li><Link to="/upload">Upload Documents</Link></li>
            <li><a href="#">Time tracking</a></li>
          </ul>
        </div>
        <div className="footer-section">
          <h3>Information</h3>
          <ul>
            <li><a href="#">FAQ</a></li>
            <li><a href="#">Documentation</a></li>
          </ul>
        </div>
        <div className="footer-section">
          <h3>Company</h3>
          <ul>
            <li><a href="#">About us</a></li>
            <li><a href="#">Contact us</a></li>
          </ul>
        </div>
        <div className="footer-section">
          <h3>Questions or Concerns?</h3>
          <input type="email" placeholder="Email address" />
          <button>-</button>
        </div>
      </div> */}
    </>
  );
}

export default Directory;
