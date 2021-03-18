<!-- View for student to plan their desired grade and keep on track -->
<template>
  <div class="main">
    
    <div v-if="true" style="margin-top: 8pt;"> 
      <sui-form v-if="role != 'professor'" @submit.prevent>
        <sui-form-field v-if="true">
          <h2
            data-toggle="tooltip"
            data-placement="bottom"
            :title="'Input your desired letter grade and date to have everything submitted'">
            Target
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-question-circle" viewBox="0 0 16 16">
              <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"></path>
              <path d="M5.255 5.786a.237.237 0 0 0 .241.247h.825c.138 0 .248-.113.266-.25.09-.656.54-1.134 1.342-1.134.686 0 1.314.343 1.314 1.168 0 .635-.374.927-.965 1.371-.673.489-1.206 1.06-1.168 1.987l.003.217a.25.25 0 0 0 .25.246h.811a.25.25 0 0 0 .25-.25v-.105c0-.718.273-.927 1.01-1.486.609-.463 1.244-.977 1.244-2.056 0-1.511-1.276-2.241-2.673-2.241-1.267 0-2.655.59-2.75 2.286zm1.557 5.763c0 .533.425.927 1.01.927.609 0 1.028-.394 1.028-.927 0-.552-.42-.94-1.029-.94-.584 0-1.009.388-1.009.94z"></path>
            </svg>
          </h2>
          <label>Grade</label>
          <sui-dropdown
            placeholder="Select desired grade"
            @input="calculate(); log();"
            :options="this.grade_collection"
            selection
            search
            v-model="target_grade"
          />
          <label>Month</label>
          <sui-dropdown
            placeholder="Select desired month due"
            @input="calculate();"
            :options="this.month_collection"
            selection
            search
            v-model="month"
          />
          <label>Day</label>
          <sui-dropdown
            placeholder="Select desired day due"
            @input="calculate();"
            :options="this.day_collection"
            selection
            search
            v-model="day"
          />
          
          
        </sui-form-field>
        <br>
        <!--<button type="button" class="btn btn-create" @click="removeDupStudentToAssignment()">Add/Update Grade</button>-->
      </sui-form>

      <!-- Standing -->
      <h2 class="alignleft">Standing</h2>
      <sui-table celled >
        <sui-table-header>
        <sui-table-row>
          <sui-table-header-cell :width="2"></sui-table-header-cell>
          <sui-table-header-cell :width="2">Mastered</sui-table-header-cell>
          <sui-table-header-cell :width="2">Competency</sui-table-header-cell> 
        </sui-table-row>
        </sui-table-header>
        <sui-table-body>        
        <sui-table-row>
          <sui-table-cell>Current ({{letterGrade}})</sui-table-cell>
          <sui-table-cell>{{ numNodesMast }}</sui-table-cell>
          <sui-table-cell>{{ numNodesComp }}</sui-table-cell>
        </sui-table-row>
        <sui-table-row>
          <sui-table-cell>Target ({{this.gradeToLetter(target_grade)}})</sui-table-cell>
          <sui-table-cell> {{ target_mastered }} </sui-table-cell>
          <sui-table-cell> {{ target_comp }} </sui-table-cell>
        </sui-table-row>
        </sui-table-body>
      </sui-table>

      <!-- Plan -->
      <h2 class="alignleft">Plan</h2>
      <sui-table celled >
        <sui-table-header>
        <sui-table-row>
          <sui-table-header-cell :width="2"></sui-table-header-cell>
          <sui-table-header-cell :width="2">Mastered</sui-table-header-cell>
          <sui-table-header-cell :width="2">Competency</sui-table-header-cell> 
        </sui-table-row>
        </sui-table-header>
        <sui-table-body>        
        <sui-table-row>
          <sui-table-cell>Need</sui-table-cell>
          <sui-table-cell>{{ mast_needed }}</sui-table-cell>
          <sui-table-cell>{{ comp_needed }}</sui-table-cell>
        </sui-table-row>
        <sui-table-row>
          <sui-table-cell>Pace (per week)</sui-table-cell> <!-- TODO: Have a switch form perweek to per day if pace > 7 -->
          <sui-table-cell>{{ ((days_diff != null) ? (mast_needed/(days_diff/(7))).toFixed(2) : 'None') }}</sui-table-cell>
          <sui-table-cell>{{ ((days_diff != null) ? (comp_needed/(days_diff/7)).toFixed(2) : 'None') }}</sui-table-cell>
        </sui-table-row>
        <sui-table-row>
          <sui-table-cell>Recommendation</sui-table-cell> <!-- TODO: Insert recomended assignments -->
          <sui-table-cell> <a>Link to assign</a> </sui-table-cell>
          <sui-table-cell> <a>Link to assign</a> </sui-table-cell>
        </sui-table-row>
        </sui-table-body>  
      </sui-table>
    </div>
    <h2 v-else>
      Failed to get grade data
    </h2>

  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapMutations } from 'vuex';
import { API_URL } from '@/constants';

export default {
  components: {
    
  },
  props: {
    role: {
      type: String,
      default: 'professor',
    },
    data: {
      type: Object,
    },
    id: {
      type: String,
      required: true,
    },
    letterGrade: {
      type: String,
      required: true,
    }, 
    numNodesComp: { // TODO: Refactor - These may not all be needed. Maybe can be made smaller
      type: Number,
      required: true,
    },
    numNodesMast: {
      type: Number,
      required: true,
    },
    graphData: {},
  },
  data() {
    return {
      competency_thresholds: {},
      grade_thresholds: {},

      target_grade: null,
      target_mastered: '?',
      target_comp: '?',
      grade_collection: [],
      letters: ['A','B','C','D'],
      additions: ['+','','-'],

      mast_needed: 'None',
      comp_needed: 'None',

      // Used for target date
      months: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
      month_collection: [],
      month: null,
      days: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
      day_collection: [],
      day: null,
      days_diff: null,

    };
  },
  mounted() {
    this.retrieveResources();
    this.setGrades();
    this.setDates();
    console.log(JSON.stringify(this.graphData, null,4));
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    // TODO: Refactor this and include is as a prop rather than 
    retrieveResources() {
      const profile = JSON.parse(localStorage.getItem('profile'));
      axios.get(`${API_URL}/courses/${this.id}/competency-threshold`, { headers: { Authorization: `Bearer ${profile.auth.profile.id_token}` } })
        .then((comp) => {
          this.competency_thresholds = comp.data.result;
          delete this.competency_thresholds.pk;
          delete this.competency_thresholds.course;
        });
      axios.get(`${API_URL}/courses/${this.id}/grade-threshold`, { headers: { Authorization: `Bearer ${profile.auth.profile.id_token}` } })
        .then((grade) => {
          this.grade_thresholds = grade.data.result;
          delete this.grade_thresholds.pk;
          delete this.grade_thresholds.course;
        });
    },
    addToStr(add) {
      if (add === '+')
        return '_plus';
      if (add === '-')
        return '_minus';
      return '';
    },
    strToAdd(str) {
      if (str === 'plus')
        return '+';
      if (str === 'minus')
        return '-';
      return '';
    },
    gradeToLetter(grade) {
      if (grade == null)
        return '?';
      let temp = grade.split('_');
      let ret = '';
      if (temp.length > 0)
        ret += temp[0].toUpperCase();
      if (temp.length > 1)
        ret += this.strToAdd(temp[1]);
      return ret;
    },
    setGrades() {
      this.letters.forEach(letter => {
        this.additions.forEach(add => {
          this.grade_collection.push({value:letter.toLowerCase()+this.addToStr(add),text:letter+add});
        });
      });
    },
    calculate() {
      this.target_mastered = this.grade_thresholds[this.target_grade+'_mastery'];
      this.target_comp = this.grade_thresholds[this.target_grade+'_competency'];
      
      this.mast_needed = (this.target_mastered-this.numNodesMast);
      this.comp_needed = (this.target_comp-this.numNodesComp);
      if (this.mast_needed < 0 && this.comp_needed > 0)
        this.comp_needed += this.mast_needed;
      this.comp_needed = (this.comp_needed > 0) ? this.comp_needed : 0;
      

      if (this.target_grade != null && this.month != null && this.day != null) {
        let now = new Date();
        let goal = new Date(now.getFullYear(),this.month,this.day);
        this.days_diff = Math.ceil((goal.getTime() - now.getTime())/(1000 * 3600 * 24));
        console.log(this.days_diff);
        console.log(this.mast_needed/(this.days_diff/(7)));
        
      }
    },
    log() {
      console.log(this.target_grade + ' ' + this.target_mastered + ' ' + this.target_comp);

    },
    setDates() {
      let m = 0;
      this.months.forEach(month => {
        this.month_collection.push({value:m,text:month});
        m++;
      });
      this.days.forEach(day => {
        this.day_collection.push({value:day,text:day+''});
      });
    }
    
  }
};

</script>

<style scoped>
  .topic-modal {
    position: absolute;
    top: 0;
    left: 0;
    z-index: 1000000;
    width: 100%;
    height: 100%;
    background-color: rgba(100, 100, 100, 0.8);
  }
  .topic-modal > .content {
    grid-area: content;

    background-color: #fff;
    -webkit-box-shadow: 0 0.75pt 1.5pt 0 rgba(34,36,38,.15);
    box-shadow: 0 0.75pt 1.5pt 0 rgba(34,36,38,.15);
    border: 0.75pt solid rgba(34,36,38,.15);
    padding: 8pt;
    border-radius: 6pt;
    
    margin: auto;
    width: 70%;
    min-width: 525pt;
    height: 95%;

    position: relative;
    top: 50%;
    transform: perspective(0.75pt) translateY(-50%);
    padding: 18pt;

    display: grid;
    grid-template-areas: 
    'title exit'
    'tabnav tabnav'
    'main main';
    grid-template-rows: min-content min-content 1fr;
    grid-template-columns: 1fr min-content;
  }

  .topic-modal > .content > .title {
    grid-area: title;
  }
  .topic-modal > .content > .tab-nav {
    grid-area: tabnav;
  }
  .topic-modal > .content > .main {
    grid-area: main;
  }

  .close-modal-button {
    cursor: pointer;
    grid-area: exit;
  }
  .close-modal-button:hover {
    color: var(--color-blue);
  }

  .selected {
    background-color:lightgreen;
  }
  h2 {
    padding: 5px;
    margin:0;
  }
  h3 {
    padding: 5px;
    margin:0;
  }
  .alignleft {
	float: left;
  }
  .alignright {
	float: right;
  }
</style>