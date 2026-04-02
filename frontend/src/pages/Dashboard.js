import {React, useEffect, useState} from "react";
import { Link } from "react-router-dom";
import Header from "../components/Header";
import "../Dashboard.css";
import "../Directory.css";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import Footer from "../components/Footer";
import axios from "axios";



function Dashboard() {
const [caseCounts, setCaseCounts] = useState([]);
  
const [cases, setCases] = useState([]);

const data = caseCounts?.map(caseCount=>({
     
  name: caseCount.casesyear, value: caseCount.casescount 
  // { name: "2", value: 400 },
  // { name: "3", value: 500 },
  // { name: "4", value: 450 },
  // { name: "5", value: 600 },
  // { name: "6", value: 800 },
  // { name: "7", value: 750 },
  // { name: "8", value: 650 },
  // { name: "9", value: 500 },
  // { name: "10", value: 450 },

}));


const getAllCases=()=>{

  axios.get("http://localhost:5000/case-detail/1").then((res)=>{
    setCases(res.data)

  })
}

const getAllCaseCounts=()=>{

  axios.get("http://localhost:5000/case-count/").then((res)=>{
    setCaseCounts(res.data)

  })
}

 useEffect(()=>{
  getAllCases();
  getAllCaseCounts();
  document.title="Dashboard";
  
}, []);


  



  return (
    
    <>
    
      <Header />
      <div className="dashboard-container">
        <h1 className="dashboard-title">Fraud Dashboard</h1>

        <div className="stats-container">
          <div className="stat-card">
            <h3>Active Case Count</h3>
            <p className="stat-number">45 <span className="green">▼ -6</span></p>
          </div>
          <div className="stat-card">
            <h3>Current Positive Fraud Count</h3>
            <p className="stat-number">12 <span className="red">▲ +4</span></p>
          </div>
          <div className="stat-card">
            <h3>Annual Fraud Increase</h3>
            <p className="stat-number">26% <span className="red">▲ +3%</span></p>
          </div>
          <div className="stat-card">
            <h3>Cases Solved</h3>
            <p className="stat-number">25 <span className="green">▲ +3</span></p>
          </div>
        </div>

        <div className="dashboard-main">
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={data}>
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <CartesianGrid stroke="#ccc" />
                <Line type="monotone" dataKey="value" stroke="#d9534f" strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="sidebar">
            <Link to="/case-listings">
            <button className="sidebar-btn">Case Listings <img src="/list.svg" alt="List" className="folder-icon" /> </button>
            </Link>
            <Link to="/upload">
            <button className="sidebar-btn">Case File Upload<img src="/open folder.svg" alt="Upload Folder" className="folder-icon" /> </button>
            </Link>
            <Link to="/activity-log">
            <button className="sidebar-btn">Activity Log <br></br><br></br><img src="/bell.png" alt="notification bell" className="notification-icon" /></button>
            </Link>
          </div>
        </div>

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
             <tr>
                <td><Link to={"/case-detail/" + cases.id} className="case-link">{cases.casename}</Link></td>
                <td>{cases.date}</td>
                <td>{cases.docketnum}</td>
                <td>{cases.description}</td>
                <td>{cases.casetype}</td>
                <td><span className="status ongoing">🟡 {cases.status}</span></td>
              </tr> 
            </tbody>
          </table>
        </div>
        <Footer />
      </div>
    </>
  );
}

export default Dashboard;
