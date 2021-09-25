import React from 'react';
import {makeStyles} from "@material-ui/core/styles";
import {Card, CardHeader, Divider, SvgIcon, Grid, Box} from "@material-ui/core";
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';

// Source: https://materialdesignicons.com/
import { mdiCakeVariant } from '@mdi/js';


const useStyles = makeStyles({
    root: { 
      maxHeight: 220,
      minWidth: 370,
    }, 
    header: {
      backgroundColor: "rgb(100, 174, 217)",
    },
    padding: {
      paddingRight: "100px",
    },
    box: {
      padding: "3px",
    }
  });

export default function AboutCom(props) {
  const classes = useStyles();
  let date = new Date(props.createdAt).toDateString();

  return (
    <Box>
      <Card className={classes.root}>
        <CardHeader className={classes.header}
          title={
            <Typography variant="h5" component="h2">
              About Community
            </Typography>
          }
        />

        <CardContent>
          <Box className={classes.box}>
            <Typography variant="subtitle1" component="h2">
              {props.description}
            </Typography>
          </Box>

          <Box className={classes.box}>
            <Grid container direction='row'>
              <Grid item direction='column'>
                <Grid item>
                  <Typography>{props.members}</Typography>
                </Grid>
                <Grid item className={classes.padding}>
                  Members
                </Grid>
              </Grid>
            </Grid>
          </Box>

          <Divider/>  

          <Box className={classes.box}>
            <Grid container direction='row' spacing={1}>
              <Grid item>
                <SvgIcon ><path d={mdiCakeVariant} /></SvgIcon>
              </Grid>
              <Grid item>
                <Typography>Created at {date}</Typography>
              </Grid>
            </Grid>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
} 