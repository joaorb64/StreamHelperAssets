import "./App.css";
import React, { useEffect, useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { ListGroup } from "react-bootstrap";
import { FaEye, FaDownload } from "react-icons/fa";
import { GiFloatingPlatforms } from "react-icons/gi";
import { Link, useParams } from "react-router-dom";

export default function AssetPack(props) {
  const [, updateState] = React.useState();
  const forceUpdate = React.useCallback(() => updateState({}), []);

  const { game, pack } = useParams();
  const [baseFiles, setBaseFiles] = useState(null);
  const [asset, setAsset] = useState(null);
  const [characterData, setCharacterData] = useState({});
  const [gameFiles, setGameFiles] = useState([]);
  const [skinSelection, setSkinSelection] = useState({});

  useEffect(() => {
    console.log(game);
    console.log(pack);
    GetBaseFiles();
    GetAsset();
  }, [game, pack]);

  const GetAsset = () => {
    let assetName = pack;
    if (assetName == "base_files") {
      assetName = "base_files/icon";
    }
    return fetch(
      `https://raw.githubusercontent.com/joaorb64/StreamHelperAssets/main/games/${game}/${assetName}/config.json`
    )
      .then((response) => response.json())
      .then((responseJson) => {
        setAsset(responseJson);
        console.log(responseJson);
      })
      .catch((error) => {
        console.error(error);
      });
  };

  const GetBaseFiles = () => {
    return fetch(
      `https://raw.githubusercontent.com/joaorb64/StreamHelperAssets/main/games/${game}/base_files/config.json`
    )
      .then((response) => response.json())
      .then((responseJson) => {
        setBaseFiles(responseJson);
        console.log(responseJson);
      })
      .catch((error) => {
        console.error(error);
      });
  };

  const getAssetKey = (assetFile) => {
    let key = "character_to_codename";
    if (assetFile && assetFile.type) {
      if (assetFile.type.includes("stage_icon")) {
        key = "stage_to_codename";
      }
    }
    return key;
  };

  useEffect(() => {
    setCharacterData({});
    if (asset && baseFiles) {
      let key = getAssetKey(asset);

      let assetName = pack;

      if (assetName == "base_files") {
        assetName = "base_files/icon";
      }

      fetch(
        `https://api.github.com/repos/joaorb64/StreamHelperAssets/contents/games/${game}/${assetName}`
      )
        .then((response) => response.json())
        .then((responseJson) => {
          console.log(responseJson);
          setGameFiles(responseJson);

          let prefix = asset.prefix ? asset.prefix : "";
          let postfix = asset.postfix ? asset.postfix : "";

          let allData = {};

          Object.entries(baseFiles[key]).forEach(([name, charData]) => {
            allData[charData.codename] = charData;
            allData[charData.codename].name = name;

            let characterAssets = responseJson.filter((entry) =>
              entry.name.startsWith(`${prefix}${charData.codename}${postfix}`)
            );

            allData[charData.codename].images = {};

            for (const [i, image] of characterAssets.entries()) {
              let data = {
                src: image,
              };

              let skinIndex = 0;

              try {
                let number = image.name.replace(
                  `${prefix}${charData.codename}${postfix}`,
                  ""
                );
                number = number.split(".")[0];
                number = parseInt(number);
                if (!isNaN(number)) skinIndex = number;
              } catch (e) {
                console.log(e);
              }

              if (asset.eyesights && asset.eyesights[charData.codename]) {
                if (asset.eyesights[charData.codename][i]) {
                  data.eyesight = asset.eyesights[charData.codename][i];
                } else if (asset.eyesights[charData.codename][0]) {
                  data.eyesight = asset.eyesights[charData.codename][0];
                }
              }

              data.width = 256;
              data.height = 256;

              allData[charData.codename].images[skinIndex] = data;
            }
            skinSelection[charData.codename] = 0;
            LoadAsset(charData, 0);
          });

          setCharacterData(allData);
        })
        .catch((error) => {
          console.error(error);
        });
    }
  }, [asset, baseFiles, game, pack]);

  const LoadAsset = (characterData, skin) => {
    let file = characterData.images[skin];

    if (file) {
      if (!file.src.name.endsWith("webm")) {
        let img = new Image();
        img.src = file.src.download_url;

        img.onload = () => {
          if (characterData.images[skin]) {
            characterData.images[skin].width = img.naturalWidth;
            characterData.images[skin].height = img.naturalHeight;
            characterData.images[skin].url = img.src;
            // setCharacterData(data);
            forceUpdate();
            // console.log(data);
          }
        };
      } else {
        if (characterData.images[skin]) {
          characterData.images[skin].video = file.src.download_url;
          // setCharacterData(data);
          forceUpdate();
        }
      }
    }
  };

  return (
    <div>
      <h3>
        /{game}/{pack}
      </h3>

      {props.games && game in props.games ? (
        <ListGroup style={{ marginTop: 16, marginBottom: 16 }}>
          {Object.entries(props.games)
            .filter((g) => g[0] == game)
            .map(([id, game], i) => (
              <>
                <ListGroup.Item style={{ display: "flex", gap: 32 }}>
                  <div
                    style={{
                      width: 100,
                      height: 64,
                      backgroundSize: "contain",
                      backgroundRepeat: "no-repeat",
                      backgroundPosition: "center",
                      backgroundImage: `url(https://github.com/joaorb64/StreamHelperAssets/raw/main/games/${id}/base_files/logo.png)`,
                    }}
                  ></div>
                  <div
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      alignItems: "flex-start",
                    }}
                  >
                    <div
                      style={{
                        display: "flex",
                        alignItems: "baseline",
                        gap: 8,
                      }}
                    >
                      <h4>{game.name}</h4>
                      <h6>{id}</h6>
                    </div>
                    <div style={{ display: "flex", gap: "8px" }}>
                      {Object.entries(game.assets).map((asset, j) => (
                        <Link to={`/game/${id}/${asset[0]}`}>
                          <h5>
                            <span class="badge bg-primary">
                              {asset[0]}
                              {asset[1].has_eyesight_data ? (
                                <>
                                  {" "}
                                  <FaEye />
                                </>
                              ) : null}
                              {asset[1].has_stage_data ? (
                                <>
                                  {" "}
                                  <GiFloatingPlatforms />
                                </>
                              ) : null}
                            </span>
                          </h5>
                        </Link>
                      ))}
                    </div>
                  </div>
                </ListGroup.Item>
                <ListGroup.Item style={{ whiteSpace: "pre-wrap" }}>
                  <h4>Description</h4>
                  <p>{game.assets[pack].description}</p>
                </ListGroup.Item>
                <ListGroup.Item style={{ whiteSpace: "pre-wrap" }}>
                  <h4>Credits</h4>
                  <p>{game.assets[pack].credits}</p>
                </ListGroup.Item>
                <ListGroup.Item style={{ whiteSpace: "pre-wrap" }}>
                  <h4>Full pack download</h4>
                  <h5
                    style={{
                      display: "flex",
                      gap: 8,
                      justifyContent: "center",
                      alignItems: "center",
                    }}
                  >
                    {Object.keys(game.assets[pack].files).map((file, index) => (
                      <a
                        href={`https://github.com/joaorb64/StreamHelperAssets/releases/latest/download/${file}`}
                        download
                        target="_blank"
                      >
                        <span class="badge bg-primary">
                          <FaDownload /> Part {index + 1}
                        </span>
                      </a>
                    ))}
                  </h5>
                </ListGroup.Item>
              </>
            ))}
        </ListGroup>
      ) : null}

      {asset && baseFiles && characterData ? (
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "center",
          }}
        >
          {Object.entries(characterData).map(([codename, charData]) => (
            <div class="card">
              <div class="card-body">
                {charData.name != null ? (
                  <>
                    <h5 class="card-title">{charData.name}</h5>
                    <h6 class="card-subtitle text-muted">
                      {charData.codename}
                    </h6>
                    {charData.images &&
                      charData.images[skinSelection[charData.codename]] && (
                        <div>
                          <div
                            class="card mb-2 mt-2"
                            style={{ overflow: "hidden" }}
                          >
                            <div
                              style={{
                                position: "relative",
                                transformOrigin: "top left",
                                transform: charData.images[
                                  skinSelection[charData.codename]
                                ]?.video
                                  ? ""
                                  : "scale(" +
                                    Math.min(
                                      256 /
                                        charData.images[
                                          skinSelection[charData.codename]
                                        ].width,
                                      256 /
                                        charData.images[
                                          skinSelection[charData.codename]
                                        ].height
                                    ) +
                                    ")",
                                width: 256,
                                height: 256,
                              }}
                            >
                              <div
                                style={{
                                  top: 0,
                                  left: 0,
                                  width:
                                    charData.images[
                                      skinSelection[charData.codename]
                                    ]?.width,
                                  height:
                                    charData.images[
                                      skinSelection[charData.codename]
                                    ]?.height,
                                  position: "absolute",
                                }}
                              >
                                <img
                                  src={
                                    charData.images[
                                      skinSelection[charData.codename]
                                    ].url
                                  }
                                  style={{
                                    position: "absolute",
                                    top: 0,
                                    left: 0,
                                  }}
                                ></img>
                                {charData.images[
                                  skinSelection[charData.codename]
                                ].video ? (
                                  <video
                                    controls
                                    preload="metadata"
                                    width={256}
                                  >
                                    <source
                                      src={
                                        charData.images[
                                          skinSelection[charData.codename]
                                        ].video + "#t=0"
                                      }
                                    ></source>
                                  </video>
                                ) : null}
                                {charData.images[
                                  skinSelection[charData.codename]
                                ].eyesight ? (
                                  <div
                                    style={{
                                      position: "absolute",
                                      top: 0,
                                      left: 0,
                                      width: "100%",
                                      height: "100%",
                                      pointerEvents: "none",
                                    }}
                                  >
                                    <div
                                      style={{
                                        left:
                                          charData.images[
                                            skinSelection[charData.codename]
                                          ].eyesight.x - 1,
                                        width: 0,
                                        height: "100%",
                                        borderLeft: "3px solid red",
                                        position: "absolute",
                                      }}
                                    ></div>
                                    <div
                                      style={{
                                        top:
                                          charData.images[
                                            skinSelection[charData.codename]
                                          ].eyesight.y - 1,
                                        width: "100%",
                                        height: 0,
                                        borderTop: "3px solid red",
                                        position: "absolute",
                                      }}
                                    ></div>
                                  </div>
                                ) : null}
                              </div>
                            </div>
                          </div>
                          <div class="btn-group btn-group-toggle">
                            {Object.entries(charData.images || {}).map(
                              ([skin, skinData], index) => (
                                <button
                                  type="button"
                                  class={
                                    "btn btn-primary" +
                                    (skinSelection[charData.codename] == skin
                                      ? " active"
                                      : "")
                                  }
                                  onClick={() => {
                                    skinSelection[charData.codename] = skin;
                                    setSkinSelection(skinSelection);
                                    LoadAsset(charData, skin);
                                    forceUpdate();
                                  }}
                                >
                                  {skin}
                                </button>
                              )
                            )}
                          </div>
                          <p class="card-text mt-2">
                            {asset.metadata && (
                              <p class="card-subtitle text-muted">
                                {asset.metadata.map((meta) => (
                                  <>
                                    {meta.values[charData.codename] && (
                                      <div>
                                        {meta.title}:{" "}
                                        {meta.values[charData.codename].value}
                                      </div>
                                    )}
                                  </>
                                ))}
                              </p>
                            )}
                            <a
                              href={
                                charData.images[
                                  skinSelection[charData.codename]
                                ].url
                              }
                              download
                              target="_blank"
                            >
                              <span class="badge bg-primary">
                                <FaDownload /> Download
                              </span>
                            </a>
                          </p>
                        </div>
                      )}
                  </>
                ) : null}
              </div>
            </div>
          ))}
        </div>
      ) : null}
    </div>
  );
}
