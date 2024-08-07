import { transform } from '@babel/standalone';
// import MyComponent1 from './components/MyComponent1';
// import MyComponent2 from './components/MyComponent2';

export function transformJsxCodeToReactComponent(jsxCode: string) {
    // const fullCode = `
    //       (function() {
    //         const MyComponent1 = ${MyComponent1.toString()};
    //         const MyComponent2 = ${MyComponent2.toString()};
    //         return ${jsxCode};
    //       })()
    //     `;
    const fullCode = `
          (function() {
            return ${jsxCode};
          }
        )()
        `;
    const transformedCode = transform(fullCode, { presets: ['react'] }).code;
    if ((!(typeof transformedCode === 'string'))) throw new Error('transformedCode is not a string');
    const RenderedComponent = eval(transformedCode); // RenderedComponent is a jsx component
    return RenderedComponent;
}


export interface Word {
  word: string;
  start: number;
  end: number;
}

export interface Line {
  text: string;
  start?: number;
  end?: number;
  wordCount: number;
}
