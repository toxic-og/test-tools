import React from 'react';

// export default class Login extends React.Component {
//     render() {
//         return <_Login service={userService} /> 
//     }
// }

// const Login = class extends React.Component {
//     render() {
//         return <_Login service={userService} />
//     }
// }

// function inject() {
//     return Login
// }

// function inject() {
//     return class extends React.Component {
//         render() {
//             return <_Login service={userService} />
//         }
//     }
// }

// function inject(comp) {
//     return class extends React.Component {
//         render() {
//             return <comp service={userService} />
//         }
//     }
// }

// function inject(comp, service) {
//     return class extends React.Component {
//         render() {
//             return <comp service={service} />
//         }
//     }
// }

// function inject(comp, obj) {
//     return class extends React.Component {
//         render() {
//             return <comp {...obj} />
//         }
//     }
// }

// function inject(comp) {
//     function wrapper(obj) {
//         return class extends React.Component {
//             render() {
//                 return <comp {...obj} />
//             }
//         }
//     }
//     return wrapper
// }

// const inject = function (comp) {
//     return function wrapper(obj) {
//         return class extends React.Component {
//             render() {
//                 return <comp {...obj} />
//             }
//         }
//     }
// }

// const inject = obj => Comp =>class extends React.Component {
//     render() {
//         return <Comp {...obj} />
//     }
// }

const inject = obj => Comp => props => <Comp {...obj} {...props}/>

export {inject};



