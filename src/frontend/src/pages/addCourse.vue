<template>
  <div class="addCourse">
    <h2>Add a course</h2>
    <div class="content">
      <div id="current-courses">Current Courses:
        <div></div>
        <!--print courses (right now just premade) -->
        <div
          id="courses"
          v-for="course in courses"
          :key="course.name"
          class="course"
        >{{ course.name }}</div>
        <div>
          <p></p>
          <!-- formatting instructions -->
          <p>Formatting for CSV file:</p>
          <p>first line: course declairation</p>
          <p>coursename, coursecode, subjectcode EX. (datastructures, 2150, subjectcode)</p>
          <p>second line: topic declairation</p>
          <p>topicname, childoftopic, childoftopic, childoftopic</p>
          <p></p>
        </div>
        <div id="name-change">Upload a course (CSV):</div>

        <label>
          <!-- area for user to paste text for me to parse -->
          <textarea
            id="TextData"
            cols="30"
            rows="4"
            placeholder="Paste text here"
            @input="setString"
          ></textarea>
        </label>
        <!-- submit button that starts the processing of the data. -->
        <div id="buttoncontainer">
          <button
            class="submit-settings-btn submit-btn"
            :style="{
        backgroundColor: returnColor}"
            v-on:click="processString()"
          >Submit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions, mapGetters, mapMutations } from 'vuex';
import store from '../vuex';
import { Compact } from 'vue-color';
import axios from 'axios';
import { API_URL } from '@/constants';
//placeholder for hex color val
let placeholderColor = '#fff';
export default {
  name: 'addCourse',

  components: {
    Compact,
  },
  data() {
    return {
      // a bunch of variables incase I have to implement graph methods inside this page.

      courseString: null,
      //filename of uploader
      file: '',
      courseName: null,
      courseCode: null,
      subjectCode: null,
      tname: '',
      tid: '',

      topics: [],
      props: {
        data: {
          type: Object,
        },
        isOpen: {
          type: Boolean,
          required: false,
        },
        nodes: {
          type: Array,
        },
        edges: {
          type: Array,
        },
        classData: {
          type: Object,
        },
      },
      courses: [
        {
          name: 'CS 4414',
          link: 'cs-4414',
        },
        {
          name: 'CS 3205',
          link: 'cs-3205',
        },
        {
          name: 'STS 4500',
          link: 'sts-4500',
        },
      ],
    };
  },
  computed: {
    ...mapGetters(
      'settings', ['returnColor'],
      'settings', ['returnNickName'],
    ),
  },
  methods: {
    //stolen mehtods from createCourse in order to make my own course, and topics based on text data
    createCourse() {
      // Insert Post Course to DB
      // Get the ID of the professir who is logged in
      axios
        .get(`${API_URL}/students/?id_token=${this.profile.id_token}`)
        .then(res => {
          const professor_id = res.data.result.pk;

          let courseData = {
            token: this.profile.id_token,
            pk: 'None',
            name: this.courseName,
            course_code: this.courseCode,
            subject_code: this.courseSubject,
            professor: professor_id,
            nodes: {},
            edges: {},
          };
          axios
            .post(`${API_URL}/courses/`, courseData)
            .then(data => {
              axios
                .get(`${API_URL}/courses/`)
                .then(data => {
                  let courses = data.data.result;
                  let pk;
                  courses.forEach(course => {
                    if (
                      courseData.name === course.name &&
                      courseData.course_code === course.course_code &&
                      courseData.subject_code === course.subject_code
                    ) {
                      pk = course.pk;
                    }
                  });
                  this.$router.push({ name: 'Edit', params: { id: pk } });
                })
                .catch(error => {
                  console.log(error);
                });
            })
            .catch(error => {
              console.log(error);
            });
        })
        .catch(error => {
          console.log(error);
        })
        .finally(() => {
          console.log('finally');
        });
    },
    //habdle file upload
    submitFile() {
      /*
      let formData=new FormData();
      formData.append('file', this.file);
      const reader = new FileReader();
      reader.onload = event => console.log(event.target.result); // desired file content
      reader.onerror = error => reject(error);

      var res = reader.result;
      console.log("stuff: "+ reader.readAsText(this.file).substring(0, 3));
      */
      this.file = this.$refs.file.files[0];
      const reader = new FileReader();
      reader.onload = event => console.log(event.target.result); // desired file content
      reader.onerror = error => reject(error);
      reader.readAsText(this.file); // you could also read images and other binaries
      console.log(reader.result);

      /*axios.post( '/single-file',formData,
      {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
      }
    ).then(function(){
      console.log('SUCCESS!!');
    })
    .catch(function(){0000000000000000000000000000000000000000

      console.log('FAILURE!!');
    });
    */
    },
    handleFileUpload() {
      //nothing currently done here
    },
    //parsing through text
    processString() {
      console.log('Stringdata: ' + this.courseString);
      var arrayOfString = this.courseString.split(',');
      var i = 0;
      console.log(arrayOfString);
      for (i; i < arrayOfString.length; i++) {
        if (arrayOfString[i] == 'coursename') {
          this.coursename = arrayOfString[i];
          this.coursecode = arrayOfString[i + 1];
          this.subjectcode = arrayOfString[i + 2];
          i += 2;
        }
        if (arrayOfString[i] == 'topicname') {
          this.tname = arrayOfString[i + 1];
          this.tid = arrayOfString[i + 2];
          i += 1;
          createTopic();
        }
        console.log(arrayOfString[i]);
      }
      createCourse();
    },
    //method to create topic nodes.
    createTopic(event) {
      let node = {
        course: this.classData,
        grade: 0,
        id: this.tid,
        locked: false,
        student: {},
        topic: { course: this.classData.uuid, id: 'None', name: this.tname },
      };
      this.nodes.push(node);
      this.tid = '';
      this.tname = '';
      this.$emit('onClose');
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.Settings {
  height: 100%;
  width: 100%;
}
/*-webkit-box-shadow: 0pt 1.5pt 6.75pt 0pt rgba(0,0,0,0,69);
-moz-box-shadow: 0pt 1.5pt 6.75pt 0pt rgba(0,0,0,0,69);
box-shadow: 0pt*/
.content {
  font-size: 20pt;
  background-color: #fff;
  -webkit-box-shadow: 0 0.75pt 1.5pt 0 rgba(34, 36, 38, 0.15);
  box-shadow: 0 0.75pt 1.5pt 0 rgba(34, 36, 38, 0.15);
  border: 0.75pt solid rgba(34, 36, 38, 0.15);
  padding: 30pt;
  border-radius: 6pt;
  height: 90%;
  width: 80%;
  margin-left: auto;
  margin-right: auto;
}
.color-change {
  padding: 3%;
  height: 5%;
  font-size: 12.75pt;
  margin-top: 10pt;
}
.submit-btn {
  margin: auto;
  width: 40%;
  height: 40%;
  max-width: 250pt;
  max-height: 50pt;
  color: blue;
  border-radius: 18.75pt;
  font-size: 12pt;
  border: none;
  padding: 8pt 18pt;
  cursor: pointer;
  outline: none;
  margin-top: 20%;
  margin-left: 35%;
  border: 1.5pt solid black;
}
#courses {
  margin-top: 2%;
  font-size: 11.25pt;
}
#enter-coursedata {
  width: 80%;
  height: 120%;
}
</style>
