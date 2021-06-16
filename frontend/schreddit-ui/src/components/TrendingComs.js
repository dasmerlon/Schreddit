import React from 'react';
import {makeStyles} from "@material-ui/core/styles";
import {Card, Avatar, List, ListItem, ListItemAvatar, ListItemSecondaryAction, ListItemText, Button, Typography, Link, CardHeader} from "@material-ui/core"

const useStyles = makeStyles((theme) => ({
    root: {
      width: '100%',
      maxWidth: 400,
      maxHeight: 445,
    },
  }));

export default function TrendingComs() {
    const classes = useStyles();
  
    return (
        <Card className={classes.root}>
            <CardHeader title="Trending Communities" />
            <List >
                <ListItem>
                    <ListItemAvatar>
                    <Avatar
                        alt={`Avatar`}
                        src={`/static/images/avatar/1.jpg`}
                    />
                    </ListItemAvatar>
                    <ListItemText
                        primary={
                            <Link href="#"  color="inherit">
                                {'r/sharks'}
                            </Link>
                        }
                        secondary={
                            <Typography
                                variant="body2"
                                color="textPrimary"
                            >
                                32,000 Members
                            </Typography>
                        }
                    />
                    <ListItemSecondaryAction>
                        <Button variant="contained" color="primary">join</Button>
                    </ListItemSecondaryAction>
                </ListItem>
                <ListItem>
                    <ListItemAvatar>
                    <Avatar
                        alt={`Avatar`}
                        src={`/static/images/avatar/4.jpg`}
                    />
                    </ListItemAvatar>
                    <ListItemText
                        primary={
                            <Link href="#"  color="inherit">
                                {'r/sharks'}
                            </Link>
                        }
                        secondary={
                            <Typography
                                variant="body2"
                                color="textPrimary"
                            >
                                32,000 Members
                            </Typography>
                        }
                    />
                    <ListItemSecondaryAction>
                        <Button variant="contained" color="primary">join</Button>
                    </ListItemSecondaryAction>
                </ListItem>
                <ListItem>
                    <ListItemAvatar>
                    <Avatar
                        alt={`Avatar`}
                        src={`/static/images/avatar/1.jpg`}
                    />
                    </ListItemAvatar>
                    <ListItemText
                        primary={
                            <Link href="#"  color="inherit">
                                {'r/sharks'}
                            </Link>
                        }
                        secondary={
                            <Typography
                                variant="body2"
                                color="textPrimary"
                            >
                                32,000 Members
                            </Typography>
                        }
                    />
                    <ListItemSecondaryAction>
                        <Button variant="contained" color="primary">join</Button>
                    </ListItemSecondaryAction>
                </ListItem>
                <ListItem>
                    <ListItemAvatar>
                    <Avatar
                        alt={`Avatar`}
                        src={`/static/images/avatar/1.jpg`}
                    />
                    </ListItemAvatar>
                    <ListItemText
                        primary={
                            <Link href="#"  color="inherit">
                                {'r/sharks'}
                            </Link>
                        }
                        secondary={
                            <Typography
                                variant="body2"
                                color="textPrimary"
                            >
                                32,000 Members
                            </Typography>
                        }
                    />
                    <ListItemSecondaryAction>
                        <Button variant="contained" color="primary">join</Button>
                    </ListItemSecondaryAction>
                </ListItem>
                <ListItem>
                    <ListItemAvatar>
                    <Avatar
                        alt={`Avatar`}
                        src={`/static/images/avatar/1.jpg`}
                    />
                    </ListItemAvatar>
                    <ListItemText
                        primary={
                            <Link href="#"  color="inherit">
                                {'r/sharks'}
                            </Link>
                        }
                        secondary={
                            <Typography
                                variant="body2"
                                color="textPrimary"
                            >
                                32,000 Members
                            </Typography>
                        }
                    />
                    <ListItemSecondaryAction>
                        <Button variant="contained" color="primary">join</Button>
                    </ListItemSecondaryAction>
                </ListItem>
            </List>
        </Card>
    );
  }

  