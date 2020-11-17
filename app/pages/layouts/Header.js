import Head from 'next/head';

import { Navbar, Nav, NavDropdown } from 'react-bootstrap';

const Header = () => (
    <div style={{
        marginBottom: '5%'
    }}>
      <Head>
        <title>Accounting Notebook App</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Navbar fixed="top" collapseOnSelect expand="lg" bg="dark" variant="dark">
            <Navbar.Brand href="/">Accounting Notebook</Navbar.Brand>
            <Navbar.Toggle aria-controls="responsive-navbar-nav" />
            <Navbar.Collapse id="responsive-navbar-nav">
                <Nav>
                    <NavDropdown title="options" id="collasible-nav-dropdown">
                        <NavDropdown.Item href="/history">history</NavDropdown.Item>
                        <NavDropdown.Item href="/movement">add movement</NavDropdown.Item>
                        <NavDropdown.Divider />
                        <NavDropdown.Item href="/about-us">about us</NavDropdown.Item>
                    </NavDropdown>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
        <br />
    </div>
  );
  
  export default Header;