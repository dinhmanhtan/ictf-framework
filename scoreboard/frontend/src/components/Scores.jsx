import React, { Component } from 'react';
import { findDOMNode } from 'react-dom';
import c3 from 'c3';
import _ from 'underscore';

import api from '../sources/api';
import SetIntervalMixin from '../mixins/SetIntervalMixin';
import round from '../utils/round';
import Table from './shared/Table';
import Flag from './shared/Flag';

const POLLING_INTERVAL = 10 * 1000;

class Scores extends Component {
  state = {
    lastScores: [],
    lastScoresSorted: [],
    teamsShown: 'top',
    services: []
  }

  constructor() {
    /* don't use state for scores, c3 is rendered outside React */
    super();
    this.ticks = [];
    this.chart_ref = React.createRef();
  }

  /* FIXME: double fetch, check App component */
  loadTicks(ticksCount) {
    api.get('/game/state', {n_ticks: ticksCount}).then(res => {
      this.setState({services: res.body.static.services})
      let lastTick = this.ticks[this.ticks.length-1]; 
      if (res.body.dynamic.length > 0 && (!lastTick || lastTick.tick.tick_id !== res.body.dynamic[0].tick.tick_id)) {
        const serviceDict = Object.entries(res.body.static.services).map(([key, value]) => ({ [key]: value.service_name }));
        let lastScores = _.values(res.body.dynamic[0].scores);
        lastScores = lastScores.map(s => {
          let data = {team_id: s.team_id,total_points:s.total_points}
          for (const obj of serviceDict) {
            for (const [service_id, service_name] of Object.entries(obj)) {
                  data[service_name] = s[service_id.toString()]
            }
          }

          data.team_name = res.body.static.teams[s.team_id] && res.body.static.teams[s.team_id].name;
          return data;
        });
        this.ticks = this.ticks.concat(res.body.dynamic);
        this.setState({
          lastScores: lastScores,
          lastScoresSorted: this.sortScores(lastScores, 'total_points')
        });
      }
    });
  }

  sortScores(scores, sortAttribute) {
    let sortedScores = _.chain(scores).values().sortBy(sortAttribute).reverse().value();
    return sortedScores;
  }

  componentDidMount() {
    this.loadTicks(20);
    // this.chart = c3.generate({
    //   bindto: findDOMNode(this.chart_ref),
    //   legend: {
    //     show: true
    //   },
    //   data: {
    //     x: 'x',
    //     rows: [['x']]

    //   },
    //   tooltip: {
    //     show: false
    //   },
    //   axis: {
    //     y: {
    //       show: false
    //     },
    //     x: {
    //       type: 'line'
    //     }
    //   }
    // });
    this.setInterval(() => this.loadTicks(1), POLLING_INTERVAL);
  }

  componentDidUpdate() {
    let teamsNames = _.pluck(_.first(this.state.lastScoresSorted, 10), 'team_name');
    let teamsIds = _.pluck(_.first(this.state.lastScoresSorted, 10), 'team_id');
    let scores = this.ticks.map(tick => {
      var pickedScores = [];
      for (var idx in teamsIds) {
        pickedScores.push(tick.scores[teamsIds[idx]]);
      }
      let points = _.pluck(pickedScores, 'total_points');
      return [tick.tick.tick_id].concat(points);
    });
    scores.unshift(
      ['x'].concat(teamsNames)
    );
    // this.chart.load({
    //   rows: scores
    // });
    // this.chartShowTeams();
  }

  // chartShowTeams() {
  //   if (this.state.teamsShown === 'all') {
  //     this.chart.show && this.chart.show();
  //   }
  //   else if (this.state.teamsShown === 'none') {
  //     this.chart.hide && this.chart.hide() && this.chart.hide();
  //   } else if (this.state.teamsShown === 'top') {
  //     this.chartShowTop();
  //   }
  // }

  // chartShowTop() {
  //   this.chart.hide();
  //   let firstScores = _.first(this.state.lastScoresSorted, 10);
  //   let teamNames = firstScores.map(k => {
  //     let team = _.find(this.props.teams, f => {
  //       if (f.id === k.team_id) {
  //         return true;
  //       }
  //     });
  //     return team && team.name;
  //   });
  //   this.chart.show(teamNames);
  // }

  // handleChartToggle(type, e) {
  //   e.preventDefault();
  //   this.setState({teamsShown: type});
  // }

  tableHeaders() {

    const serviceNames = this.state.services ? Object.values(this.state.services).map(service => {
      //console.log(service.service_name.replace(/_/g, ' '))
      return service.service_name.replace(/_/g, ' ')
    }) : [];
    let tableHeaders = [
      {id: 'team_rank', label: 'Rank', className: 'width--64-on-desk'},
      {id: 'team_name', label: 'Team', altSortAttr: 'team_name_sort'},
    ]
    for (let i = 0; i < serviceNames.length; i++) {
      const serviceName = serviceNames[i];
      tableHeaders.push({id:serviceName,label:serviceName})
    }
    tableHeaders.push({id: 'total_points',label:'Total Score'})
    return tableHeaders

  }

  tableRows() {
    console.log("",this.state.lastScoresSorted)
    const serviceNames = this.state.services ? Object.values(this.state.services).map(service => service.service_name.replace(/_/g, ' ')) : []
    return this.state.lastScoresSorted.filter(score => {
      return Object.values(this.props.teams).find(t => t.id === score.team_id);
    }).map((s, i) => {
      let team = Object.values(this.props.teams).find(t => t.id === s.team_id);
      let teamNameTag = (
        <div style={{display:"flex",flexDirection: "row",alignItems:"center"}}>
          <div style={{marginRight:"5px"}}><Flag country={ team.country } size="21"  /></div> 
          <div>{ team.name }</div>
        </div>);
      let flags = (
        <div> 
          <div style={{display:"flex",flexDirection: "row",alignItems:"center"}}>
            <div style={{width:"12px"}}>+</div> 
            <div>{s.exploited_flags}</div>
          </div> 
          <div style={{display:"flex",flexDirection: "row",alignItems:"center"}}>
            <div style={{width:"12px",fontSize:"1.5rem"}} >-</div>
            <div>{s.lost_flags} </div> 
          </div>
        </div>)
      let data = {
        team_rank: i + 1,
        team_name_sort: team.name.toLowerCase(),
        team_name: teamNameTag,

      };
      for (const serviceName of serviceNames) {
        let service_score = s[serviceName.replace(/ /g, "_")];
        
        const exploited_flags = (service_score && service_score.exploited_flags !== undefined) ? service_score.exploited_flags : "0";
        const lost_flags = (service_score && service_score.lost_flags !== undefined ) ? service_score.lost_flags : "0";
        const attack_points = (service_score && service_score.attack_points !== undefined ) ? service_score.attack_points : "0";
        const defense_points = (service_score && service_score.defense_points !== undefined ) ? service_score.defense_points : "0";
        const sla_points = (service_score && service_score.sla_points !== undefined ) ? service_score.sla_points : "0";
        let row = (
          <div> 
            <div style={{display:"flex",flexDirection: "row",alignItems:"center"}}>
              <div style={{width:"40px"}}>A/T:</div> 
              <div>{attack_points}</div>
            </div> 
            <div style={{display:"flex",flexDirection: "row",alignItems:"center"}}>
              <div style={{width:"40px"}} >D/F:</div>
              <div>{defense_points} </div> 
            </div>
            <div style={{display:"flex",flexDirection: "row",alignItems:"center"}}>
              <div style={{width:"40px"}} >SLA:</div>
              <div>{sla_points} </div> 
            </div>
            <div style={{display:"flex",flexDirection: "row",alignItems:"center"}}>
              <div style={{width:"40px"}} >Flag:</div>

              <div style={{display:"flex",flexDirection: "row",alignItems:"center"}}> 

                <div style={{display:"flex",flexDirection: "row",alignItems:"center",marginRight:"2px"}}>
                  <div>+</div> 
                  <div>{exploited_flags}</div>
                </div>
                / 
                <div style={{display:"flex",flexDirection: "row",alignItems:"center",marginLeft:"2px"}}>
                  <div style={{fontSize:"1.5rem"}} >-</div>
                  <div>{lost_flags} </div> 
                </div>

              </div>

            </div>
          </div>)
        data[serviceName] = row
      }

      data.total_points = s.total_points;
      return data
    });
  }

  render() {
    return (
      <div>
        <h3 className="title">Scoreboard</h3>
       {/* <div className="chart" ref={this.chart_ref}/> 
        <nav className="chart-controls">
          <a href="#" onClick={ this.handleChartToggle.bind(this, 'all') }>Show all</a>
              <span> - </span>
              <a href="#" onClick={ this.handleChartToggle.bind(this, 'none') }>Hide all</a>
              <span> - </span>
          <a href='#top10' onClick={ this.handleChartToggle.bind(this, 'top') }>
            Top 10
          </a>
        </nav> */}

        <Table headers={ this.tableHeaders() }
               rows={ this.tableRows() }
               defaultSortAttr={ 'team_rank' }
               defaultSortDirection={ 'asc' }
               className={ 'space--top-1' }/>
      </div>
    );
  }
}
Scores = SetIntervalMixin(Scores);
export default Scores;
