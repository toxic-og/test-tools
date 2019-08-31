import React from 'react';
import {postService as service} from '../service/user';
import {observer} from 'mobx-react';
import {inject} from '../utils';
import {message, Card} from 'antd';

import 'antd/lib/message/style';
import 'antd/lib/card/style';

@inject({service})
@observer
export default class Detail extends React.Component {
    constructor (props) {
        super(props);
        let {id=-1} = props.match.params;
        this.props.service.getDetail(id);
    }
    render() {
        let msg = this.props.service.msg;
        const {title='',content='', author, postdate} = this.props.service.detail;
        if(title) {
            return(
                <Card title={title} bordered={false} style={{width:300}}>
                    <p>{author} {new Date (postdate*1000).toDateString()} </p>
                    <p>{content}</p>
                </Card>
            )
        }
        else
            return(<div>无数据</div>)
    }
    componentDidUpdate(prevProps, prevState) {
        if(prevProps.service.msg) {
            message.info(prevProps.service.msg, 3, () => prevProps.service.msg='')
        }
    }
}