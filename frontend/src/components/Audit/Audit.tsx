import React from "react";
import { useParams } from "react-router";

export const Audit = () => {
  let { websiteURL } = useParams();

  return <div>{websiteURL}</div>;
};
