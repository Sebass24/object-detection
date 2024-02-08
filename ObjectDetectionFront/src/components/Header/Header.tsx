import { Nav } from "react-bootstrap"
import { Container } from "react-bootstrap"
import { Navbar } from "react-bootstrap"
import Logo from "./Logo/Logo.tsx"

export const Header = () => {

  return (
    <>
      <Navbar bg="light" variant="light" fixed="top">
        <Container>
          <Navbar.Brand href="/">TESIS</Navbar.Brand>
          <Nav className="me-auto">
            <Nav.Link href="/">Upload</Nav.Link>
            <Nav.Link href="/imageList">Lista de imagenes</Nav.Link>
          </Nav>
          <Nav className="ml-auto">
            <Logo />
          </Nav>
        </Container>
      </Navbar>
    </>
  )

}