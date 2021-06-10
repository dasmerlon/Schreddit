import React from 'react';
import { withStyles, makeStyles } from '@material-ui/core/styles';
import MuiAccordion from '@material-ui/core/Accordion';
import MuiAccordionSummary from '@material-ui/core/AccordionSummary';
import MuiAccordionDetails from '@material-ui/core/AccordionDetails';
import Typography from '@material-ui/core/Typography';
import { Button, Grid, Link } from '@material-ui/core';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

const Accordion = withStyles({
  root: {
    border: '1px solid rgba(0, 0, 0, .125)',
    boxShadow: 'none',
    '&:not(:last-child)': {
      borderBottom: 0,
    },
    '&:before': {
      display: 'none',
    },
    '&$expanded': {
      margin: 'auto',
    },
  },
  expanded: {},
})(MuiAccordion);

const AccordionSummary = withStyles({
  root: {
    backgroundColor: 'rgba(0, 0, 0, .03)',
    borderBottom: '1px solid rgba(0, 0, 0, .125)',
    marginBottom: -1,
    minHeight: 56,
    '&$expanded': {
      minHeight: 56,
    },
  },
  content: {
    '&$expanded': {
      margin: '12px 0',
    },
  },
  expanded: {},
})(MuiAccordionSummary);

const AccordionDetails = withStyles((theme) => ({
  root: {
    padding: theme.spacing(2),
  },
}))(MuiAccordionDetails);

const useStyles = makeStyles ({
    root: {
        maxHeight: 530,
    }
});

export default function PopularComs() {
  const classes = useStyles();

  const [expanded, setExpanded] = React.useState('panel1');

  const handleChange = (panel) => (event, newExpanded) => {
    setExpanded(newExpanded ? panel : false);
  };

  return (
    <div className={classes.root}>
      <Accordion square expanded={expanded === 'panel1'} onChange={handleChange('panel1')}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel1d-content" id="panel1d-header">
          <Typography>POPULAR COMMUNITIES</Typography>
        </AccordionSummary>
        <AccordionDetails>
            <Grid container direction="column" spacing={1}>
                <Grid item container direction="row" spacing={1}> 
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"AskReddit"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"NoStupidQuestions"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"DestinyTheGame"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"explainlikeimfive"} </Link>
                    </Grid>
                </Grid>
                <Grid>
                    <Button color="primary" variant="text" >
                        See more
                    </Button>
                </Grid>
            </Grid>
        </AccordionDetails>
      </Accordion>
      <Accordion square expanded={expanded === 'panel2'} onChange={handleChange('panel2')}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel2d-content" id="panel2d-header">
          <Typography>GAMING</Typography>
        </AccordionSummary>
        <AccordionDetails>
            <Grid container direction="column" spacing={1}>
                <Grid item container direction="row" spacing={1}> 
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"StardewValley"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"FortniteCompetitve"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"Warframe"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"totalwar"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"Fallout"} </Link>
                    </Grid>
                </Grid>
                <Grid>
                    <Button color="primary" variant="text" >
                        See more
                    </Button>
                </Grid>
            </Grid>
        </AccordionDetails>
      </Accordion>
      <Accordion square expanded={expanded === 'panel3'} onChange={handleChange('panel3')}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel3d-content" id="panel3d-header">
          <Typography>SPORTS</Typography>
        </AccordionSummary>
        <AccordionDetails>
            <Grid container direction="column" spacing={1}>
                <Grid item container direction="row" spacing={1}> 
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"running"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"soccer"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"MMA"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"hockey"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"formula1"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"CFB"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"barstoolsports"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"airsoft"} </Link>
                    </Grid>
                </Grid>
                <Grid>
                    <Button color="primary" variant="text" >
                        See more
                    </Button>
                </Grid>
            </Grid>
        </AccordionDetails>
      </Accordion>
      <Accordion square expanded={expanded === 'panel4'} onChange={handleChange('panel4')}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel4d-content" id="panel4d-header">
          <Typography>TV</Typography>
        </AccordionSummary>
        <AccordionDetails>
            <Grid container direction="column" spacing={1}>
                <Grid item container direction="row" spacing={1}> 
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"Naruto"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"BokuNoHeroAcademia"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"marvelstudios"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"rupaulsdragrace"} </Link>
                    </Grid>
                </Grid>
                <Grid>
                    <Button color="primary" variant="text" >
                        See more
                    </Button>
                </Grid>
            </Grid>
        </AccordionDetails>
      </Accordion>
      <Accordion square expanded={expanded === 'panel5'} onChange={handleChange('panel5')}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel5d-content" id="paneld-header">
          <Typography>TRAVEL</Typography>
        </AccordionSummary>
        <AccordionDetails>
            <Grid container direction="column" spacing={1}>
                <Grid item container direction="row" spacing={1}> 
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"vancouver"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"brasil"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"australia"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"mexico"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"argentina"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"melbourne"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"ottawa"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"korea"} </Link>
                    </Grid>
                </Grid>
                <Grid>
                    <Button color="primary" variant="text" >
                        See more
                    </Button>
                </Grid>
            </Grid>
        </AccordionDetails>
      </Accordion>
      <Accordion square expanded={expanded === 'panel6'} onChange={handleChange('panel6')}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel6d-content" id="panel6d-header">
          <Typography>HEALTH & FITNESS</Typography>
        </AccordionSummary>
        <AccordionDetails>
            <Grid container direction="column" spacing={1}>
                <Grid item container direction="row" spacing={1}> 
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"orangetheory"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"bodybuilding"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"bodyweightfitness"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"vegan"} </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"crossfit"} </Link>
                    </Grid>
                </Grid>
                <Grid>
                    <Button color="primary" variant="text" >
                        See more
                    </Button>
                </Grid>
            </Grid>
        </AccordionDetails>
      </Accordion>
      <Accordion square expanded={expanded === 'panel7'} onChange={handleChange('panel7')}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel7d-content" id="panel7d-header">
          <Typography>FASHION</Typography>
        </AccordionSummary>
        <AccordionDetails>
            <Grid container direction="column" spacing={1}>
                <Grid item container direction="row" spacing={1}> 
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"MakeupAddiction"} </Link>
                        </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"Watches"} </Link>
                        </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"BeautyGuruChatter"} </Link>
                        </Grid>
                    <Grid item>
                        <Link href="#" variant="subtitle1" color="inherit"> {"femalefashionadvice"} </Link>
                    </Grid>
                </Grid>
                <Grid>
                    <Button color="primary" variant="text" >
                        See more
                    </Button>
                </Grid>
            </Grid>
        </AccordionDetails>
      </Accordion>
    </div>
  );
}
