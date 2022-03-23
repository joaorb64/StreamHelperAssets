import './App.css';
import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { ListGroup } from 'react-bootstrap';
import { FaEye } from 'react-icons/fa';
import { GiFloatingPlatforms } from 'react-icons/gi';

class GameList extends React.Component {

  render() {
    return (
      <div>
        <h1>Supported games</h1>
        <ListGroup>
          {Object.entries(this.props.games).map(([id, game], i)=>(
             <ListGroup.Item style={{display: "flex", gap: 32}}>
              <div style={{
                width: 100, height: 64,
                backgroundSize: "contain", backgroundRepeat: "no-repeat", backgroundPosition: "center",
                backgroundImage: `url(https://github.com/joaorb64/StreamHelperAssets/raw/main/games/${id}/base_files/logo.png)`
              }}></div>
              <div style={{display: "flex", flexDirection: "column", alignItems: "flex-start"}}>
                <div style={{display: "flex", alignItems: "baseline", gap: 8}}>
                  <h4>{game.name}</h4><h6>{id}</h6>
                </div>
                <div style={{display: 'flex', gap: "8px"}}>
                  {Object.entries(game.assets).map((asset, j)=>(
                    <h5>
                      <span class="badge bg-primary">
                        {asset[0]}
                        {asset[1].has_eyesight_data ? 
                          <>{" "}<FaEye /></>
                          :
                          null
                        }
                        {asset[1].has_stage_data ? 
                          <>{" "}<GiFloatingPlatforms /></>
                          :
                          null
                        }
                      </span>
                    </h5>
                  ))}
                </div>
              </div>
            </ListGroup.Item>
          ))}
        </ListGroup>
      </div>
    )
  };
}

export default GameList;
