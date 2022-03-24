import './App.css';
import React, { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { ListGroup } from 'react-bootstrap';
import { FaEye } from 'react-icons/fa';
import { GiFloatingPlatforms } from 'react-icons/gi';
import { useParams } from 'react-router-dom';

export default function AssetPack() {

  const [, updateState] = React.useState();
  const forceUpdate = React.useCallback(() => updateState({}), []);

  const {game, pack} = useParams();
  const [baseFiles, setBaseFiles] = useState(null)
  const [asset, setAsset] = useState(null)
  const [imageSizes, setImageSizes] = useState({})

  useEffect(()=>{
    console.log(game)
    console.log(pack)
    GetBaseFiles();
    GetAsset();
  }, [])

  const GetAsset = () => {
    let assetName = pack;
    if(assetName == "base_files"){
      assetName = "base_files/icon";
    }
    return fetch(`https://raw.githubusercontent.com/joaorb64/StreamHelperAssets/main/games/${game}/${assetName}/config.json`)
    .then((response) => response.json())
    .then((responseJson) => {
      setAsset(responseJson);
      console.log(responseJson);
    })
    .catch((error) => {
      console.error(error);
    });
  }

  const GetBaseFiles = () => {
    return fetch(`https://raw.githubusercontent.com/joaorb64/StreamHelperAssets/main/games/${game}/base_files/config.json`)
    .then((response) => response.json())
    .then((responseJson) => {
      setBaseFiles(responseJson);
      console.log(responseJson);
    })
    .catch((error) => {
      console.error(error);
    });
  }

  useEffect(()=>{
    if(asset && baseFiles){
      Object.entries(baseFiles.character_to_codename).forEach(([name, charData])=>{
        let assetName = pack;
        if(assetName == "base_files"){
          assetName = "base_files/icon";
        }

        let prefix = asset.prefix ? asset.prefix : "";
        let postfix = asset.postfix ? asset.postfix : "";

        ["", "0", "00"].forEach((skinName)=>{
          let img = new Image();
          img.src = `https://github.com/joaorb64/StreamHelperAssets/raw/main/games/${game}/${assetName}/${prefix}${charData.codename}${postfix}${skinName}.png`;
  
          img.onload = ()=>{
            imageSizes[charData.codename] = {
              width: img.naturalWidth,
              height: img.naturalHeight,
              url: img.src
            };
            setImageSizes(imageSizes);
            forceUpdate();
          }
        })
      })
    }
  }, [asset, baseFiles, game, pack])

  return (
    <div>
      <h3>{game}/{pack}</h3>

      {asset && baseFiles && imageSizes ?
        <div style={{display: "flex", flexWrap: "wrap", justifyContent: "center"}}>
          {Object.entries(baseFiles.character_to_codename).map(([name, charData])=>(
            <div class="card">
              <div class="card-body">
                {imageSizes[charData.codename] != null ?
                  <>
                  <h5 class="card-title">{name}</h5>
                  <h6 class="card-subtitle mb-2 text-muted">{charData.codename}</h6>
                  <div class="card">
                    <div style={{
                      position: "relative",
                      transformOrigin: "top left",
                      transform: "scale("+Math.min( 
                        256 / imageSizes[charData.codename].width, 
                        256 / imageSizes[charData.codename].height 
                      )+")",
                      width: 256,
                      height: 256
                    }}>
                      <div style={{
                        top: 0,
                        left: 0,
                        width: imageSizes[charData.codename].width,
                        height: imageSizes[charData.codename].height,
                        position: "absolute",
                        backgroundSize: "contain",
                        backgroundPosition: "center",
                        backgroundRepeat: "no-repeat",
                        backgroundImage: `
                          url(${imageSizes[charData.codename].url})
                        `
                      }}>
                        {asset.eyesights && asset.eyesights[charData.codename] ?
                          <div style={{position: "absolute", top: 0, left: 0, width: "100%", height: "100%"}}>
                            <div style={{
                              left: Object.values(asset.eyesights[charData.codename])[0].x-1,
                              width: 0,
                              height: "100%",
                              borderLeft: "3px solid red",
                              position: "absolute"
                            }}></div>
                            <div style={{
                              top: Object.values(asset.eyesights[charData.codename])[0].y-1,
                              width: "100%",
                              height: 0,
                              borderTop: "3px solid red",
                              position: "absolute"
                            }}></div>
                          </div>
                          :
                          null
                        }
                      </div>
                    </div>
                  </div>
                  </>
                  :
                  null
                }
              </div>
            </div>
          ))}
        </div>
        :
        null
      }
    </div>
  )
}
