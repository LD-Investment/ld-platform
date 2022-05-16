import React from "react";
import LdAxios from "ld-axios/axios";
import { Card, Col, Row } from "@themesberg/react-bootstrap";

export default () => {
  return (
    <>
      <div className="d-flex py-2" />
      <Row className="justify-content-md-left">
        <h4>Recent news</h4>
        <Col xs={8} className="mb-4">
          <Col xs={8} className="mb-4"></Col>
          <Card
            border="light"
            className="shadow-sm card-lift-hover"
            onClick={() => onClick(id)}
            style={{ cursor: "pointer" }}
          >
            <Card.Body>
              날짜 기간 지정 코인 선택 - 드롭다운, 값을 비트코인 한개만 News
              scroll
            </Card.Body>
          </Card>
        </Col>
        <Col xs={4} className="mb-4">
          bull bear neutral help
        </Col>
      </Row>
    </>
  );
};
