import { cloneDeep } from "lodash";
export const deepCopy = cloneDeep;

export const isEmpty = (obj) =>
  [Object, Array].includes((obj || {}).constructor) &&
  !Object.entries(obj || {}).length;

export const isNil = (value) => {
  return value === null || value === undefined || value === "";
};
