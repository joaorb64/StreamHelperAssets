import './App.css';
import GameList from './GameList';
import React from 'react';
import { Container, Nav, Navbar, NavDropdown } from 'react-bootstrap';
import { BrowserRouter, HashRouter, Route, Routes, Link } from 'react-router-dom';
import AssetPack from './AssetPack';

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
        <HashRouter>
          <Navbar bg="dark" variant="dark" expand="lg">
            <Container>
              <Navbar.Brand href="/">StreamHelperAssets</Navbar.Brand>
              <Navbar.Toggle aria-controls="basic-navbar-nav" />
              <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="me-auto">
                  <Nav.Link as={Link} to={"/"}>Home</Nav.Link>
                  <Nav.Link href={"https://github.com/joaorb64/StreamHelperAssets"}>GitHub</Nav.Link>
                </Nav>
              </Navbar.Collapse>
            </Container>
          </Navbar>
          <Container className='p-4'>
            <Routes>
              <Route exact path="/" element={
                this.state.gameList ? 
                  <GameList games={this.state.gameList} />
                  :
                  null
                }>
              </Route>
              <Route path="/game/:game/:pack" element={
                this.state.gameList ? 
                  <AssetPack games={this.state.gameList}></AssetPack>
                  :
                  null
                }>
              </Route>
            </Routes>
          </Container>
        </HashRouter>
      </div>
    );
  }
}

export default App;
