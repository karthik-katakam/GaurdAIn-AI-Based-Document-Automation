import {React, useState, useEffect} from 'react';
import { useParams } from 'react-router-dom';
import Header from '../components/Header';
import Footer from "../components/Footer";
import { Link } from 'react-router-dom';

function ActivityLog() {
  let { id } = useParams();

  return (
    <>
    <Header />
    {/*All this data will be grabbed by database */}
    <h1> <center>Activity Log</center></h1>
    <div className="case-listings">
             <table style={{backgroundColor:"white" }} >
               <thead>
                 <tr>
                   <th>Time & Date</th>
                   <th>Activity</th>
                   <th>Author</th>
                 </tr>
               </thead>
               <td>2011-10-10T14:48:00 </td>
               <td>EZ-accounting form uploaded  </td>
               <td>Sam Jones </td>

             </table>

    </div>
    <Footer/>
    </>
  );
}

export default ActivityLog;