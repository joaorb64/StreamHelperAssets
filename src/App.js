import './App.css';
import GameList from './GameList';
import React from 'react';
import { Container, Nav, Navbar, NavDropdown } from 'react-bootstrap';

class App extends React.Component {

  constructor(props){
    super(props);
    
    this.state = {
      gameList: null
    }
  }

  componentDidMount(){
    this.GetGameList();
  }

  GetGameList() {
    return fetch('https://raw.githubusercontent.com/joaorb64/StreamHelperAssets/main/assets.json')
    .then((response) => response.json())
    .then((responseJson) => {
      this.setState({gameList: responseJson});
      console.log(this.state.gameList)
    })
    .catch((error) => {
      console.error(error);
    });
  }

  render() {
    return (
      <div className="App">
        <Navbar bg="dark" variant="dark" expand="lg">
          <Container>
            <Navbar.Brand href="#home">StreamHelperAssets</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="me-auto">
                <Nav.Link href="#home">Home</Nav.Link>
                <Nav.Link href="#link">Link</Nav.Link>
                <NavDropdown title="Dropdown" id="basic-nav-dropdown">
                  <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
                  <NavDropdown.Item href="#action/3.2">Another action</NavDropdown.Item>
                  <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
                  <NavDropdown.Divider />
                  <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item>
                </NavDropdown>
              </Nav>
            </Navbar.Collapse>
          </Container>
        </Navbar>
        <Container className='p-4'>
          {this.state.gameList ? 
            <GameList games={this.state.gameList} />
            :
            null
          }
        </Container>
      </div>
    );
  }
}

export default App;
