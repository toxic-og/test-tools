import React from 'react';
import ReactDom from 'react-dom';
import {Route, Link, BrowserRouter as Router} from 'react-router-dom';
import {Menu, Icon, Layout} from 'antd';
import {Home} from './component/home';
import {About} from './component/about';
import Reg from './component/reg';
import Login from './component/login';
import Pub from './component/pub';
import L from './component/list';
//import Post from './component/post';

import 'antd/lib/menu/style';
import 'antd/lib/icon/style';
import 'antd/lib/layout/style';

const {Header, Content, Footer} = Layout;

const App = () => (
  <Router>
    <Layout>
      <Header>
        <Menu mode='horizontal' theme='dark'>
          <Menu.Item key='home'><Link to='/'><Icon type='home' />主页</Link></Menu.Item>
          <Menu.Item key='login'><Link to='/login'><Icon type='login' />登录</Link></Menu.Item>
          <Menu.Item key='reg'><Link to='/reg'><Icon type='user' />注册</Link></Menu.Item>
          <Menu.Item key='pub'><Link to='/pub'><Icon type='edit' />发布</Link></Menu.Item>
          <Menu.Item key='list'><Link to='/list'><Icon type='bars' />文章列表</Link></Menu.Item>
          <Menu.Item key='about'><Link to='/about'><Icon type='phone' />联系我们</Link></Menu.Item>
        </Menu>
      </Header>
      
      <Content style={{padding:'8px 50px'}}>
        <div style={{background:'#fff', padding:24, minHeight:280}}>
          <Route exact path='/' component={Home} />
          <Route path='/about' component={About} />
          <Route path='/login' component={Login} />
          <Route path='/reg' component={Reg} />
          <Route path='/pub' component={Pub} />
          <Route path='/list' component={L} />
        </div>
      </Content>

      <Footer style={{textAlign:'center'}}>
        博客系统@2019-8
      </Footer>
    </Layout>
        
  </Router>
);
ReactDom.render(<App />, document.getElementById('root'))













