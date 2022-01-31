import React from "react";
import { Col, Row } from "@themesberg/react-bootstrap";
import { UserSettingForm } from "../../components/Forms";

export default () => {
  return (
    <>
      <Row>
        <Col xs={12} xl={8}>
          <UserSettingForm />
        </Col>
      </Row>
    </>
  );
};
