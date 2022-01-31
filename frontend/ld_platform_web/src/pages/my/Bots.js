import React from "react";

import { SubscribedBotTable } from "../../components/Tables";

export default () => {
  return (
    <>
      <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center py-4">
        <div className="d-block mb-4 mb-md-0">
          <h4>Subscribed Bots</h4>
        </div>
      </div>
      <SubscribedBotTable />
    </>
  );
};
