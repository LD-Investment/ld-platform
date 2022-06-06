import React from "react";
import { Button, Card, Col, Form, Row } from "@themesberg/react-bootstrap";

export const UserSettingForm = () => {
  return (
    <Card border="light" className="bg-white shadow-sm mb-4">
      <Card.Body>
        <h5 className="mb-4">General information</h5>
        <Form>
          <Row>
            <Col md={6} className="mb-3">
              <Form.Group id="firstName">
                <Form.Label>First Name</Form.Label>
                <Form.Control
                  required
                  type="text"
                  placeholder="Enter your first name"
                />
              </Form.Group>
            </Col>
            <Col md={6} className="mb-3">
              <Form.Group id="lastName">
                <Form.Label>Last Name</Form.Label>
                <Form.Control
                  required
                  type="text"
                  placeholder="Also your last name"
                />
              </Form.Group>
            </Col>
          </Row>

          <h5 className="my-4">Exchange information</h5>
          <Row>
            <Col sm={4} className="mb-3">
              <Form.Group id="city">
                <Form.Label>Name</Form.Label>
                <Form.Select id="state" defaultValue="0">
                  <option value="0">Binance</option>
                  <option value="AL">Upbit</option>
                </Form.Select>
              </Form.Group>
            </Col>{" "}
            <Col sm={4}>
              <Form.Group id="zip">
                <Form.Label>API Key</Form.Label>
                <Form.Control required type="tel" placeholder="-" />
              </Form.Group>
            </Col>
            <Col sm={4}>
              <Form.Group id="zip">
                <Form.Label>API Secret</Form.Label>
                <Form.Control required type="tel" placeholder="-" />
              </Form.Group>
            </Col>
          </Row>
          <div className="mt-3">
            <Button variant="primary" type="submit">
              Save All
            </Button>
          </div>
        </Form>
      </Card.Body>
    </Card>
  );
};
