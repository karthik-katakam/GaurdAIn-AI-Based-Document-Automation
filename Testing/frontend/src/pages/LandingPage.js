import { React, useEffect} from 'react';
import { Link } from 'react-router-dom';
import Header from '../components/Header';
import Footer from "../components/Footer";


function LandingPage() {
   useEffect(()=>{
    
        document.title="GuardAInship Watch";
        <link rel="icon" href="/favicon.ico"/>
      }, []);
      
  return (
    
    <>
    <Header />
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      {/* Main Content Section */}
      <div style={{ flex: '1', display: 'flex', justifyContent: 'space-around', alignItems: 'center', padding: '50px' }}>
        <div style={{ textAlign: 'left', maxWidth: '40%' }}>
          <h1 style={{ fontSize: '3em', marginBottom: '20px' }}>Detect Fraud and Enforce Integrity</h1>
          <p style={{ fontSize: '1.1em', marginBottom: '30px' }}>Explore a state of the art Fraud Detector utilizing machine learning to identify suspicious inconsistencies in Guardianship cases.</p>
          <Link to="/directory">
            <button style={{ padding: '12px 25px', background: '#267144', color: 'white', border: 'none', borderRadius: '5px', fontSize: '1em', cursor: 'pointer', boxShadow: '0px 2px 2px 2px rgba(0, 0, 0, 0.25)'  }}>GET STARTED</button>
          </Link>
        </div>
        <div style={{ maxWidth: '40%' }}>
          <img src="/guardAInWatch (1).png" alt="GuardAIn Watch Logo" style={{ width: '100%' }} />
        </div>
      </div>

      {/* Bottom Section */}
      <Footer/>
      {/* <div style={{ padding: '30px', background: '#f0f0f0', display: 'flex', justifyContent: 'space-around', alignItems: 'flex-start', borderTop: '1px solid #ccc', fontSize: '0.9em' }}>
        <div>
          <h3 style={{ marginBottom: '15px' }}>Product</h3>
          <p>Case Listings</p>
          <p>Dashboard</p>
          <p>Upload Documents</p>
          <p>Time Tracking</p>
        </div>
        <div>
          <h3 style={{ marginBottom: '15px' }}>Information</h3>
          <p>FAQ</p>
          <p>Documentation</p>
          <p>GitHub</p>
        </div>
        <div>
          <h3 style={{ marginBottom: '15px' }}>Company</h3>
          <p>About Us</p>
          <p>Contact Us</p>
        </div>
        <div style={{ maxWidth: '25%' }}>
          <h3 style={{ marginBottom: '15px' }}>Questions or Concerns?</h3>
          <input type="email" placeholder="Email address" style={{ width: '100%', padding: '8px', marginBottom: '10px', border: '1px solid #ccc', borderRadius: '5px' }} />
          <button style={{ padding: '8px 15px', background: '#007bff', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>→</button>
        </div>
      </div> */}

      {/* Footer */}
      {/* <div style={{ padding: '10px', textAlign: 'center', background: '#e0e0e0', fontSize: '0.8em' }}>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <span style={{ marginRight: '10px' }}>Logo</span>
          <span style={{ marginRight: '10px' }}>Terms</span>
          <span style={{ marginRight: '10px' }}>Privacy</span>
          <span style={{ marginRight: '10px' }}>Cookies</span>
          <span>in</span>
        </div>
      </div> */}
    </div>
    </>
  );
}

export default LandingPage;