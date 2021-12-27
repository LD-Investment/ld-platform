import React from "react";
import { faCashRegister, faChartLine } from "@fortawesome/free-solid-svg-icons";
import { Col, Row } from "@themesberg/react-bootstrap";

import { CounterWidget } from "../../components/Widgets";

export default () => {
  return (
    <>
      <div className="d-flex py-2" />
      <Row className="justify-content-md-left">
        <h4>Available Bots</h4>
        <Col xs={12} sm={6} xl={4} className="mb-4">
          <CounterWidget
            category="Indicator Bot"
            title="AI News Detector"
            period="21/08/11 ~ Present"
            percentage={18.2}
            icon={faChartLine}
            iconColor="shape-secondary"
          />
        </Col>

        <Col xs={12} sm={6} xl={4} className="mb-4">
          <CounterWidget
            category="Indicator Bot"
            title="AI News Stream2"
            period="21/03/24 ~ Present"
            percentage={28.4}
            icon={faCashRegister}
            iconColor="shape-tertiary"
          />
        </Col>
      </Row>
    </>
  );
};
