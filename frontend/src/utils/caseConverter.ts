import _ from "lodash";

export const keysToCamel = (obj: any): any => {
  if (Array.isArray(obj)) {
    return obj.map((v) => keysToCamel(v));
  } else if (obj !== null && obj.constructor === Object) {
    return Object.entries(obj).reduce(
      (acc, [key, value]) => ({
        ...acc,
        [_.camelCase(key)]: keysToCamel(value),
      }),
      {},
    );
  }
  return obj;
};
