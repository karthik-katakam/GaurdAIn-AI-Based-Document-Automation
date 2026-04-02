import React, { useState, useEffect } from 'react';
import SearchBar from './SearchBar';
import { Link } from 'react-router-dom';
import "../index.css"
import { Container, Navbar, Nav} from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';



function Header() {
  useEffect(()=>{
  
      document.title="GuardAInship Watch";
      <link rel="icon" href="/gavel-solid.ico"/>
    }, []);
  return (
    <header className="header">
      <head>

      </head>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}> {/* Changed justifyContent */}
      <Link to="/" className="header-link"><img src = "/guardAInTextFinalLogo.png" alt="logo" className="logo"></img></Link>
      </div>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <Navbar className='navbar' expand="lg" >
            <Container className='navContainer' >
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav" >
              <Nav className='me-auto'>
                <div style={{marginTop:'10px'}}>
              <Link to="/" className="header-link" style={{ margin: '0 20px', cursor: 'pointer' }}>HOME</Link>
              <Link to="/dashboard" className="header-link" style={{ margin: '0 20px', cursor: 'pointer' }}>DASHBOARD</Link>
              <Link to="/directory" className="header-link" style={{ margin: '0 20px', cursor: 'pointer' }}>DIRECTORY</Link>
              <Link to="/case-listings" className="header-link" style={{ paddingRight: '0px', margin: '0 20px', cursor: 'pointer' }}>CASE LISTINGS</Link>
              </div>
              <img src = "/magnifying_glass.svg" alt="magnifying_glass" className="notification-icon"  style={{  margin: '0 10px', cursor: 'pointer' }}></img>
              <SearchBar   style={{  padding: '0 45px', cursor: 'pointer' }}/>
              <img src = "/bell.svg" alt="bell" className="notification-icon"  style={{ margin: '0 30px', cursor: 'pointer' }}></img>
              </Nav>
            </Navbar.Collapse>
            </Container>
            </Navbar>
        </div>
    </header>
    
  );
}

export default Header;