import React from 'react';
import {Card, SvgIcon} from "@material-ui/core";
import CardActions from '@material-ui/core/CardActions';
import Button from '@material-ui/core/Button';

//Symbols: (Source: https://material-ui.com/components/material-icons/)
import WhatshotSharpIcon from '@material-ui/icons/WhatshotSharp';
import TrendingUpRoundedIcon from '@material-ui/icons/TrendingUpRounded';
// Source: https://materialdesignicons.com/
import { mdiRocket, mdiAlertDecagram, mdiFormatVerticalAlignTop } from '@mdi/js';

//Bonus TODO: - Die verschiedenen Ansichten implementieren. ("Classic" und "Compact")
export default function SortByBar(props) {
    return (
        <Card>
            <CardActions>
                {/* <Button size="medium" title="Best" startIcon={ <SvgIcon ><path d={mdiRocket} onClick={()=>{props.getPosts('best')}} /></SvgIcon>}>Best</Button> */}
                <Button size="medium" title="New" startIcon={ <SvgIcon ><path d={mdiAlertDecagram} /></SvgIcon>} onClick={()=>{props.getPosts('new') }}>New</Button>
                <Button size="medium" title="Hot" startIcon={<WhatshotSharpIcon />} onClick={()=>{props.getPosts('hot')}}>Hot</Button>
                <Button size="medium" title="Top" startIcon={ <SvgIcon ><path d={mdiFormatVerticalAlignTop} /></SvgIcon>} onClick={()=>{props.getPosts('top') }}>Top</Button>
                {/* <Button size="medium" title="Rising" startIcon={<TrendingUpRoundedIcon />} onClick={()=>{props.getPosts('top') }}>Rising</Button> */}
            </CardActions>
        </Card>
    );
} 
