import { Link } from 'react-router-dom';
import "../index.css"
import { Container, Navbar, Nav} from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';
import '../Directory.css'
import '../Dashboard.css'

function Footer() {
return(
  <>
  <Container fluid className='footer'  >
<Navbar className='navbar' expand="lg" >
              <Container className='navContainer'>
              <Navbar.Toggle aria-controls="basic-navbar-nav" />
              <Navbar.Collapse id="basic-navbar-nav">
                <Nav className='me-auto'>
                <div className="footer-section col-12 col-lg-12">
                  <h3>Product</h3>
                  <ul>
                      <li><Link to="/case-listings">Case Listings</Link></li>
                      <li><Link to="/dashboard">Dashboard</Link></li>
                      <li><Link to="/upload">Upload Documents</Link></li>
                      <li><a href="#">Time tracking</a></li>
                  </ul>
                  </div>
    
                  </Nav>
              </Navbar.Collapse>
              </Container>
</Navbar>

<Navbar className='navbar' expand="lg" >
              <Container className='navContainer'>
              <Navbar.Toggle aria-controls="basic-navbar-nav" />
              <Navbar.Collapse id="basic-navbar-nav">
                <Nav className='me-auto'>
                <div className="footer-section col-12 col-lg-12">
                  <h3>Information</h3>
                  <ul>
                    <li><a href="#">FAQ</a></li>
                    <li><a href="#">Documentation</a></li>
                  </ul>
                </div>

                </Nav>
              </Navbar.Collapse>
              </Container>
</Navbar>


<Navbar className='navbar' expand="lg" >
              <Container className='navContainer'>
              <Navbar.Toggle aria-controls="basic-navbar-nav" />
              <Navbar.Collapse id="basic-navbar-nav">
                <Nav className='me-auto'>
                <div className="footer-section col-12 col-lg-12">
                  <h3>Company</h3>
                  <ul>
                    <li><a href="#">About us</a></li>
                    <li><a href="#">Contact us</a></li>
                  </ul>
              </div>
                </Nav>
              </Navbar.Collapse>
              </Container>
</Navbar>


<Navbar className='navbar' expand="lg" >
              <Container className='navContainer'>
              <Navbar.Toggle aria-controls="basic-navbar-nav" />
              <Navbar.Collapse id="basic-navbar-nav">
                <Nav className='me-auto'>
              <div className="footer-section col-12 col-lg-12">
                <h4>Questions or Concerns?</h4>
                <input type="email" placeholder="Email address" />
                <button className="footer-submit">→</button>
            </div>
                </Nav>
              </Navbar.Collapse>
              </Container>
</Navbar>



</Container>
<div style={{ display: 'flex', justifyContent: 'space-between', background: '#e0e0e0', alignItems: 'center' }}>
  <div style={{ flex: 1, display: 'flex', justifyContent: 'center' }}>
          <span style={{ marginRight: '10px' }}>Terms</span>
          <span style={{ marginRight: '10px' }}>Privacy</span>
          <span style={{ marginRight: '10px' }}>Cookies</span>
        </div>
        <span><a href="https://www.linkedin.com/company/njcourts/posts/?feedView=all"><img src="/linkedin.png" style={{width:"50px" }}/></a></span>
        </div>
    </>
          )}

export default Footer;