import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import Button from '@material-ui/core/Button';
import SvgIcon from '@material-ui/core/SvgIcon';
import { mdiShieldStar } from '@mdi/js';
import { CardContent } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
    root: {
        maxHeight: 195,
        minWidth: 370,
    },
}));

export default function RecipeReviewCard() {
    const classes = useStyles();

    return (
        <Card className={classes.root}>
            <CardHeader
                action={<SvgIcon fontSize="large" color="secondary"><path d={mdiShieldStar} /></SvgIcon>}
                title="Schreddit Premium"
                subheader="The best Reddit experience, with monthly Coins"
                />
            <CardContent>
                <Button variant="contained" color="secondary">
                    Try Now    
                </Button>
            </CardContent>
        </Card>
    );
}
