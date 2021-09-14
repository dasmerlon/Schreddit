import React from 'react';
import { withStyles, makeStyles } from '@material-ui/core/styles';
import MuiAccordion from '@material-ui/core/Accordion';
import MuiAccordionSummary from '@material-ui/core/AccordionSummary';
import MuiAccordionDetails from '@material-ui/core/AccordionDetails';
import Typography from '@material-ui/core/Typography';
import { CardHeader, Card } from '@material-ui/core';
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
        maxHeight: 510,
    },
    header: {
        backgroundColor: "rgb(100, 174, 217)",  
      },
});

export default function Rules() {
  const classes = useStyles();

  const [expanded, setExpanded] = React.useState('panel1');
  
  const handleChange = (panel) => (event, newExpanded) => {
    setExpanded(newExpanded ? panel : false);
  };

  return (
    <div className={classes.root}>
        <Card>
            <CardHeader className={classes.header}
                title={
                    <Typography variant="h5" component="h2">
                        Community Rules
                    </Typography>
                }
            />  
            <Accordion square expanded={expanded === 'panel1'} onChange={handleChange('panel1')}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel1d-content" id="panel1d-header">
                <Typography>1. No Toxic behavior</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    xyz
                </AccordionDetails>
            </Accordion>
            <Accordion square expanded={expanded === 'panel2'} onChange={handleChange('panel2')}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel2d-content" id="panel2d-header">
                <Typography>2. abc</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    xyz
                </AccordionDetails>
            </Accordion>
            <Accordion square expanded={expanded === 'panel3'} onChange={handleChange('panel3')}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel3d-content" id="panel3d-header">
                <Typography>3. def</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    xyz
                </AccordionDetails>
            </Accordion>
            <Accordion square expanded={expanded === 'panel4'} onChange={handleChange('panel4')}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel4d-content" id="panel4d-header">
                <Typography>4. ghi</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    xyz
                </AccordionDetails>
            </Accordion>
            <Accordion square expanded={expanded === 'panel5'} onChange={handleChange('panel5')}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel5d-content" id="paneld-header">
                <Typography>5. jkl</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    xyz
                </AccordionDetails>
            </Accordion>
            <Accordion square expanded={expanded === 'panel6'} onChange={handleChange('panel6')}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel6d-content" id="panel6d-header">
                <Typography>6. mno</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    xyz
                </AccordionDetails>
            </Accordion>
            <Accordion square expanded={expanded === 'panel7'} onChange={handleChange('panel7')}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel7d-content" id="panel7d-header">
                <Typography>7. pqr</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    xyz
                </AccordionDetails>
            </Accordion>
        </Card>
    </div>
  );
}
