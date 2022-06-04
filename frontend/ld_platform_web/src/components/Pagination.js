import React from "react";
import { Pagination } from "@themesberg/react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faAngleDoubleLeft,
  faAngleDoubleRight
} from "@fortawesome/free-solid-svg-icons";

export const CustomPagination = props => {
  const { totalPages, pageNum, setPageNum } = props;
  const [activeItem, setActiveItem] = React.useState(pageNum ? pageNum : 1);

  const onPrevItem = () => {
    const prevActiveItem = activeItem === 1 ? activeItem : activeItem - 1;
    setActiveItem(prevActiveItem);
    setPageNum(prevActiveItem);
  };

  const onNextItem = totalPages => {
    const nextActiveItem =
      activeItem === totalPages ? activeItem : activeItem + 1;
    setActiveItem(nextActiveItem);
    setPageNum(nextActiveItem);
  };

  const items = [];
  for (let number = 1; number <= totalPages; number++) {
    const isItemActive = activeItem === number;

    const handlePaginationChange = () => {
      setActiveItem(number);
      setPageNum(number);
    };

    items.push(
      <Pagination.Item
        active={isItemActive}
        key={number}
        onClick={handlePaginationChange}
      >
        {number}
      </Pagination.Item>
    );
  }

  return (
    <Pagination size="md" className="mt-3">
      <Pagination.Prev disabled={false} onClick={onPrevItem}>
        <FontAwesomeIcon icon={faAngleDoubleLeft} />
      </Pagination.Prev>
      {items}
      <Pagination.Next onClick={() => onNextItem(totalPages)}>
        <FontAwesomeIcon icon={faAngleDoubleRight} />
      </Pagination.Next>
    </Pagination>
  );
};
