// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';
import { createCanvas } from 'canvas';

HTMLCanvasElement.prototype.getContext = function (contextType) {
  if (contextType === '2d') {
    return createCanvas().getContext(contextType);
  }
  return null;
};