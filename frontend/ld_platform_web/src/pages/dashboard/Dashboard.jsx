import React from "react";
import { faChartLine } from "@fortawesome/free-solid-svg-icons";
import { Col, Row } from "@themesberg/react-bootstrap";
import LdAxios from "ld-axios/axios";
import { BotCardWidget } from "../../components/Widgets";

export default () => {
  const [bots, setBots] = React.useState([]);
  React.useEffect(() => {
    LdAxios.get("/api/bots/").then(response => {
      if (!response) return;
      setBots(response.data.data);
    });
  }, []);

  return (
    <>
      <div className="d-flex py-2" />
      <Row className="justify-content-md-left">
        <h4>Available Bots</h4>
        {bots.map((item, index) => (
          <Col xs={12} sm={6} xl={4} className="mb-4" key={index}>
            <BotCardWidget
              id={item.id}
              name={item.name_display}
              type={item.type_display}
              icon={faChartLine}
              iconColor="shape-secondary"
            />
          </Col>
        ))}
      </Row>
    </>
  );
};
