import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faGlobeEurope } from "@fortawesome/free-solid-svg-icons";
import { Card, Col, Row } from "@themesberg/react-bootstrap";
import LdAxios from "../api/axios";
import { Routes } from "../routes";

export const BotCardWidget = props => {
  const { id, name, type, version, icon, iconColor } = props;

  const onClick = botId => {
    LdAxios.post(`/api/bots/${botId}/subscribe`)
      .then(res => {
        console.log(res);
        // setLoginFailed(false);
        // // set UserStore
        // userStore.initUserInfo(res.data.data.user);
        // // redirect
        // window.location.href = `/#${Routes.PlatformDashboard.path}`;
      })
      .catch(e => {
        // setLoginFailed(true);
        throw e;
      });
  };

  return (
    <Card
      border="light"
      className="shadow-sm card-lift-hover"
      onClick={() => onClick(id)}
      style={{ cursor: "pointer" }}
    >
      <Card.Body>
        <Row className="d-block d-xl-flex align-items-center">
          <Col
            xl={4}
            className="text-xl-center d-flex align-items-center justify-content-xl-center mb-3 mb-xl-0"
          >
            <div
              className={`icon icon-shape icon-md icon-${iconColor} rounded me-4 me-sm-0`}
            >
              <FontAwesomeIcon icon={icon} />
            </div>
          </Col>
          <Col xs={12} xl={7} className="px-xl-0">
            <div className="d-none d-sm-block">
              <h5>{type}</h5>
              <h3 className="mb-1">{name}</h3>
            </div>
            <small>
              v{version} <FontAwesomeIcon icon={faGlobeEurope} size="xs" />{" "}
              web3.0
            </small>
          </Col>
        </Row>
      </Card.Body>
    </Card>
  );
};
