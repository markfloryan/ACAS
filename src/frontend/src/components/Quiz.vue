<template>
  <div>
    <div v-if="createQuiz === false && updateQuiz === false">
      <div class="quiz">
        <div class="title" style="padding:10px">
          <h3>Create or Update a quiz!</h3>
        </div>
        <div class="content">
          <h4>Select a Topic</h4>
          <sui-form-field>
            <sui-dropdown
            placeholder="Select topic"
            :options="topics"
            selection
            search
            v-model="topicPK"
            />
          </sui-form-field>
        </div>
        <div class="table">
          <sui-table v-if="assignmentToQuiz.length > 0" celled>
            <sui-table-header>
              <sui-table-row>
                <sui-table-header-cell :width="3">Name</sui-table-header-cell>
                <sui-table-header-cell :width="1">Published</sui-table-header-cell>
                <sui-table-header-cell :width="2">Actions</sui-table-header-cell>
              </sui-table-row>
            </sui-table-header>
            <sui-table-body>
              <sui-table-row
                v-for="pair in assignmentToQuiz" v-bind:key="pair.quiz.pk"
              >
                <sui-table-cell>{{ pair.assignment.name }}</sui-table-cell>
                <sui-table-cell>{{ pair.quiz.Published ? "Published" : "Not Published" }}</sui-table-cell>
                <sui-table-cell>
                  <center>
                    <button v-if="!pair.quiz.published" @click="publish(pair)" class="btn btn-create" type="button">Publish</button>
                    <button v-if="pair.quiz.published" @click="unpublish(pair)" class="btn btn-delete" type="button">Unpublish</button>
                    <button @click="editQuiz(pair)" class="btn btn-primary" type="button">Edit</button>
                    <button @click="deleteQuiz(pair)" class="btn btn-delete" type="button">Delete</button>
                  </center>
                </sui-table-cell>
              </sui-table-row>
            </sui-table-body>
          </sui-table>
        </div>
        <div class="buttons">
          <button
            class="btn btn-primary edit-btn"
            :style="returnPrimaryButtonStyle"
            style="float: right;"
            data-toggle="tooltip"
            data-placement="bottom"
            title="Create Quiz"
            @click="createQuiz = true"
          >Create a new Quiz</button>
        </div>
      </div>
    </div>
    <CreateQuiz
      v-if="createQuiz"
      :courseId="courseId"
      :topicId="topicPK"
    />
    <EditQuiz
      v-if="updateQuiz"
      :courseId="courseId"
      :assignmentQuizPair="assignmentQuizPair"
      @onClose="refresh()"
    />
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapState, mapMutations } from 'vuex';
import { API_URL } from '@/constants';
import CreateQuiz from '@/components/CreateQuiz';
import EditQuiz from '@/components/EditQuiz';

export default {
  components: { 
    CreateQuiz,
    EditQuiz
  },
  /*
  Defines the data used by the component
  */
  data(){
    return {
      topics: [],
      topicPK: null,
      quiz: null,
      createQuiz: false,
      updateQuiz: false,
      assignments: [],
      quizzes: [],
      assignmentToQuiz: [],
      assignmentQuizPair: null,
    };
  },
  mounted() {
    this.getTopics();
  },
  watch: {
    topicPK: function() {
      this.getAssignments();
    },
    assignments: function () {
      this.getQuizzes();
    },
    quizzes: function () {
      this.assignmentToQuiz = [];
      this.quizzes.forEach(quiz => {
        this.assignments.forEach(assignment => {
          if(quiz.assignment == assignment.pk) {
            this.assignmentToQuiz.push({
              assignment: assignment,
              quiz: quiz,
            });
          }
        });
      });
    },
  },
  props: {
    courseId: {
      type: String,
      required: true,
    }
  },
  computed: {
    ...mapState('auth', ['profile']),
    ...mapGetters('settings', ['returnPrimaryButtonStyle']),
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    refresh() {
      this.createQuiz = false;
      this.updateQuiz = false;
      this.getAssignments();
    },
    getTopics() {
      axios.get(`${API_URL}/topics/?courseId=${this.courseId}`, 
        { 
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${this.profile.id_token}`
          }
        }).then((response)=> {
        let data = response.data.result;
        for(let i=0;i<data.length;i++){
          let topic = data[i];
          this.topics.push({
            text: topic.name,
            value: topic.pk
          });
        }
      }).catch(function(){
        
      });
    },
    getAssignments() {
      axios.get(`${API_URL}/assignments/?topicId=${this.topicPK}`,
        { 
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${this.profile.id_token}`
          }
        }).then((response) => {
        this.assignments = response.data.result;
      });
    },
    getQuizzes() {
      axios.get(`${API_URL}/quizzes/?topicId=${this.topicPK}`,
        { 
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${this.profile.id_token}`
          }
        }).then((response) => {
        this.quizzes = response.data.result;
      });
    },
    editQuiz(pair) {
      this.assignmentQuizPair = pair;
      this.updateQuiz = true;
    },
    publish(pair) {
      let now = new Date(Date.now());
      let quizData = {
        pk: pair.quiz.pk,
        assignment: pair.quiz.assignment,
        published: true,
        next_open_date: now.toISOString(),
        next_close_date: now.toISOString(),
      };

      axios.put(`${API_URL}/quizzes/${pair.quiz.pk}`,
        quizData,
        {
          headers: {
            Authorization: `Bearer ${this.profile.id_token}`
          }
        }
      ).then((response)=> {
        if(response.data.status == '200 - OK') {
          this.openToast();
          this.setToastInfo({
            type: 'success',
            title: 'Successful publish',
            message: 'Quiz successfully published',
            duration: 5000,
          });
          this.getAssignments();
        }
      }).catch((error) => {
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Failed to publish',
          message: 'Quiz failed to publish',
          duration: 5000,
        });
      });
    },
    unpublish(pair) {
      let now = new Date(Date.now());
      let quizData = {
        pk: pair.quiz.pk,
        assignment: pair.quiz.assignment,
        published: false,
        next_open_date: now.toISOString(),
        next_close_date: now.toISOString(),
      };

      axios.put(`${API_URL}/quizzes/${pair.quiz.pk}`,
        quizData,
        {
          headers: {
            Authorization: `Bearer ${this.profile.id_token}`
          }
        }
      ).then((response)=> {
        if(response.data.status == '200 - OK') {
          this.openToast();
          this.setToastInfo({
            type: 'success',
            title: 'Successful unpublish',
            message: 'Quiz successfully unpublished',
            duration: 5000,
          });
          this.getAssignments();
        }
      }).catch((error) => {
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Failed to unpublish',
          message: 'Quiz failed to unpublish',
          duration: 5000,
        });
      });
    },
    deleteQuiz(pair) {
      axios
        .delete(`${API_URL}/quizzes/${pair.quiz.pk}`, { headers: { Authorization: `Bearer ${this.profile.id_token}` } })
        .then(response => {
          if(response.status == 200)
            this.$emit('onClose');
        })
        .catch(error => {
          console.log(error);
        });
      this.getAssignments();
    },
  }
};
</script>


<style scoped>
.quiz {
    display: grid;
    grid-template-areas:
        'title'
        'content'
        'table'
        'buttons';
    grid-template-columns: 1fr;
    grid-template-rows: 1 1 1 1;
    padding: 10pt;
}
.title {
    grid-area: title;
    padding: 10pt;
}
.content {
    grid-area: content;
    padding: 10pt;
}
.table {
    grid-area: table;
}
.buttons {
    grid-area: buttons;
    padding: 10pt;
}
</style>
