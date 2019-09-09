import React from 'react';
import {postService as service} from '../service/post';
import {observer} from 'mobx-react';
import {message, Form, Input, Button} from 'antd';
import {inject} from '../utils';

import 'antd/lib/message/style';
import 'antd/lib/Form/style';
import 'antd/lib/Icon/style';
import 'antd/lib/Input/style';
import 'antd/lib/Button/style';

const FormItem = Form.Item;
const {TextArea} = Input;

@inject({service})
@observer
export default class Pub extends React.Component {
    handleSubmit(event) {
        event.preventDefault();
        const [title, content] = event.target;
        this.props.service.pub(title.value, content.value);
    }
    render() {
        let msg = this.props.service.msg;
        const FormItemLayout = {
            labelCol:{span:2},
            wrapperCol:{span:8}
        };
        return(
            <Form layout='vertical' onSubmit={this.handleSubmit.bind(this)}>
                <FormItem label='标题:' {...FormItemLayout}>
                    <TextArea placeholder='标题'/>
                </FormItem>

                <FormItem label='内容:' {...FormItemLayout}>
                    <TextArea rows={20}/>
                </FormItem>

                <FormItem wrapperCol={{span:8 ,offset:8}}>
                    <Button type='primary' htmlType='submit'>提交</Button>
                </FormItem>
            </Form>
        )
    }

    componentDidUpdate(prevProps, prevState) {
        if(prevProps.service.msg) {
            message.info(prevProps.service.msg, 3, () => prevProps.service.msg='');
        }
    }
}