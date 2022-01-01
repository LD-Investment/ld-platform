import React from "react";
import { faCashRegister, faChartLine } from "@fortawesome/free-solid-svg-icons";
import { Col, Row } from "@themesberg/react-bootstrap";
import axios from "axios";
import { BotCardWidget } from "../../components/Widgets";

export default () => {
  const [bots, setBots] = React.useState([]);
  React.useEffect(() => {
    axios.get("/api/bots/").then(response => {
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
              name={item.name_display}
              type={item.type_display}
              version={item.version}
              period="21/08/11 ~ Present"
              percentage={18.2}
              icon={faChartLine}
              iconColor="shape-secondary"
            />
          </Col>
        ))}
      </Row>
    </>
  );
};
