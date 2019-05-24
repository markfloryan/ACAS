<template>
  <div :class="`class-graph ${ isEditGraph ? 'edit-class-graph' : null }`">
    <network
      ref="network"
      :edges="edges"
      :nodes="nodes"
      :options="options"

      :events="['click', 'dragStart', 'dragEnd', 'hoverNode', 'blurNode','onOpen']"
      @click="clickTest"
      @drag-start="mousedownOnCanvas"
      @drag-end="mouseUpOnCanvas"
      @hover-node="hoverNode"
      @blur-node="blurNode"
      @onOpen="topicModalIsOpen = true"
      @confirmOpen="confirmModal = true"
      class="network"
      :style="canvasStyle"
      ></network>
      <div class="edit actions">
        <button v-if="(!uploading) && !inEdit" @click="addEdge()" class="create-btn btn btn-create">New Edge</button>
        <button v-if="(!uploading) && !inEdit" @click="topicModalIsOpen = true" class="nodeButton btn btn-create">New Node</button>
        <button v-if="(!uploading) && !inEdit" @click="deleteMode()" class="btn btn-delete">Delete topic node</button>
        <router-link to="/">
        <button v-if="(!uploading) && !inEdit"
          @click="saveEdits()"
          :style="returnPrimaryButtonStyle"
          class="save-btn btn btn-primary"
        >Save</button>
        </router-link>
        <!--Only one button is displayed at a time, they both call different functions -->
    <input type="file" ref="file" style="display: none">
    <button v-if="!inEdit" @click="overlay()" :style="returnPrimaryButtonStyle" class="overlay-btn btn btn-primary a">Upload grades/topics</button>
    <router-link to="/">
    <button v-if="(!inEdit&&uploading)" @click="overlay()" :style="returnPrimaryButtonStyle" class="overlay-btn btn btn-primary a">Home</button>
    </router-link>
    <button v-if="inEdit&&!displayError" @click="overlay() & Calling()" :style="returnPrimaryButtonStyle" class="overlay-btn btn btn-primary b">Go back to graph editor</button>
    <button v-if="errorbutton" id="errorbutton" @click="overlay() & displayErrors()" :style="returnPrimaryButtonStyle" class="save-btn btn btn-primary b">Errors</button>
    <button v-if="inEdit&&displayError" id="errorbutton" @click="overlay() & deleteErrors()" :style="returnPrimaryButtonStyle" class="save-btn btn btn-primary b"> Back to file upload page </button>

    <div id = "overlay">
      <div style="height: 100%; overflow-y:scroll;">
        <!-- Description of course format -->
        <ul v-if='displayError' id = "Errors" style ="margin-bot:20px;">
          ERRORS: 
          <li v-for="error in Errors" :key ="error.id">
            {{error}}
          </li>
        </ul>

        <span v-if="!displayError" class = "top">
          <p>Upload topics for current course</p>
          <p>each topic is a line: </p>
          <img
            width="400px"
            src="../assets/topic.png" />
          <br />
          <br /> 
            
          <!-- button shows upload, allows user to upload file, then sumbmit sends file to file handling function -->
          <button v-if="!uploadTopicsButton" @click="$refs.file.click() & CallingTopic()" on-submit="handleFileUpload()" :style="returnPrimaryButtonStyle" class="saveTopic-btn btn btn-primary a">Upload topic CSV</button>
          <button v-if="uploadTopicsButton" id="submitbutton" @click="handleTopicUpload" class="save-btn btn btn-create">Submit topics</button>
        </span>
        <!-- button shows upload, allows user to upload file, then sumbmit sends file to file handling function (for grades) -->
        <span v-if="!displayError" class = "bottom" >
         <p>Upload grades for current course</p>
        <p>each student is a line: </p>
         <img
            width="400px"
            src="../assets/grade.png" /><br/> <br /> 
        <button v-if="!uploadGradesButton" @click="$refs.file.click() & CallingGrade()" on-submit="handleFileUpload()" :style="returnPrimaryButtonStyle" class="saveGrades-btn btn btn-primary a">Upload student grades CSV</button>
        <button v-if="uploadGradesButton" id="submitbutton" @click="handleGradesUpload" class="save-btn btn btn-create">Submit</button>
        
        </span>
      </div>
  </div> 
  <EditPopup
    :isOpen="topicModalIsOpen"
    :data="selectedNodeData"
    :edges="edges"
    :nodes="nodes"
    :classData= "classData"
    @onClose="topicModalIsOpen = false" 
    ref="editPopup" />
      <EditPopup
        :isOpen="topicModalIsOpen"
        :data="selectedNodeData"
        :edges="edges"
        :nodes="nodes"
        :classData="classData"
        @onClose="topicModalIsOpen = false"
      />
      <YouSure
        :isOpen="confirmModal"
        :data="selectedNodeData"
        @closeConfirm="confirmModal = false"
        @confirm="deleteNode()"
      />
    </div>
    <Saved :isSaved="isSaved"/>
    <h2 v-if="currentlyAddingEdge">"Click on a topic and drag arrow to a topic."</h2>
    <h2 v-if="deleteOn">"Click on the node you want to delete"</h2>
  </div>
</template>

<script>
import { Network } from 'vue2vis';
import { addNodeMode } from 'vue2vis';
import { mapGetters, mapState, mapMutations } from 'vuex';
import { generate_svg } from '@/assets/graph_node_svg.js';
import {
  edges,
  nodes as nodeData,
  options,
} from '@/assets/create_graph_data.js';
import { API_URL } from '@/constants';
import EditPopup from '@/components/EditPopup';
import Saved from '@/components/Saved';
import YouSure from '@/components/YouSure';
import axios from 'axios';

export default {
  components: {
    Network,
    EditPopup,
    YouSure,
    Saved,
  },
  props: {
    data: {},
    id: {
      type: String,
    },
    isEditGraph: {
      type: Boolean,
      default: false,
    },
    classData: {
      type: Object,
    },
  },

  data() {
    return {
      errorbutton:false,
      displayError:false,
      uploading:false,
      Errors: [],
      network: null,
      uploadGraph: false,
      layoutMethod: 'directed',
      edges: [],
      nodes: [],
      options: {},
      nEdges: {},
      selectedNodeData: {},
      topicModalIsOpen: false,
      editOn:false,
      nodeOn:false,
      courseString:null,
      file:'',
      uploadTopicsButton:false,
      uploadGradesButton:false,
      inEdit:false,
      isSaved: false,
      confirmModal: false,
      deleteOn: false,
      saved: false,
      currentlyAddingEdge: false,
      uploadButton: false,
      nameto : {},
      canvasStyle: {
        cursor: ' -webkit-grab',
      },
    };
  },
  computed: {
    ...mapState('auth', ['profile']),
    ...mapGetters('settings', ['returnPrimaryButtonStyle']),
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    //retrieves object info from clicks and calls specified function
    clickTest(data) {
      this.nodes.forEach(node => {
        if (data.nodes && data.nodes[0] === node.id) {
          this.selectedNodeData = node;
          if (this.deleteOn) {
            this.confirmModal = true;
          } else {
            this.topicModalIsOpen = true;
          }
        }
      });
    },
    //Turns delete functionality on
    deleteMode() {
      this.deleteOn = !this.deleteOn;
    },
    //Actually deletes the node
    deleteNode() {
      let pk = this.selectedNodeData.id;
      console.log(pk);
      let x = 0;
      //make sure nodes exist
      if (this.nodes.length > 0) {
        //for each node check if ids equal
        this.nodes.forEach(node => {
          console.log('target: %s, current: %s', pk, node.id);
          if (node.id == pk) {
            console.log('eq');
            let del = this.nodes.splice(x, 1);
            this.deleteOn = false;
            //if node has been saved before i.e. has a number id or saved id, delete from database
            if (Number.isInteger(pk) | (pk == 'saved')) {
              axios
                .delete(`${API_URL}/topics/${pk}`)
                .then(data => {
                  //on success print delete
                  console.log('deleted');
                  axios
                    .get(`${API_URL}/topic/topics/`)
                    .then(data => {
                      console.log('data', data);
                      let deledges = data.data.result.filter(
                        (value, index, arr) => {
                          return value.course == this.id;
                        }
                      );
                      console.log('course', deledges);
                      deledges = deledges.filter((value, index, arr) => {
                        return (
                          (value.topic_node == pk) | (value.ancestor_node == pk)
                        );
                      });
                      console.log('topic',deledges);

                      this.openToast();
                      this.setToastInfo({
                        type: 'success',
                        title: 'Successfully deleted node!',
                      });
                    })
                    .catch();
                })
                .catch(data => {
                  //on failure return -1
                  console.log(data);
                  this.openToast();
                  this.setToastInfo({
                    type: 'error',
                    title: 'There was an error deleting the node.',
                  });
                  return -1;
                });
            }
            return pk;
          } else {
            x++;
          }
        });
      } else {
        return 0;
      }
      return -1;
    },
    //Calls Warpper function for click-and-drag edge functionality; see vue2vis
    addEdge() {
      this.currentlyAddingEdge = true;
      console.log(this.$children[0]);
      this.$children[0].addEdgeMode();
      this.currentlyAddingEdge = false;
    },
    //Generates topic boxes for render
    generate_custom_graph_markup(nodeData) {
      const SVG = generate_svg();
      let nodes = nodeData;
      let nodeImage;
      nodes.forEach(node => {
        nodeImage = generate_svg(SVG, node.topic.name, node.grade, node.locked);
        node.shape = 'image';
        node.image =
          'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(nodeImage);
        node.id = node.topic.id;
      });

      return nodes;
    },
    //Zoom Out
    mousedownOnCanvas() {
      this.canvasStyle = {
        cursor: ' -webkit-grabbing',
      };
    },
    
    //Zoom in
    mouseUpOnCanvas() {
      this.canvasStyle = {
        cursor: ' -webkit-grab',
      };
    },

    //highlights nodes on hover
    hoverNode() {
      this.canvasStyle = {
        cursor: 'pointer',
      };
    },

    blurNode() {
      this.canvasStyle = {
        cursor: '-webkit-grab',
      };
    },
    displayErrors() {
      this.displayError=true;
      this.errorbutton = false;
      console.log('toggling off button and on error messages');
    },
    showerrorbutton(){
      this.errorbutton =true;
    },
    deleteErrors(){
      this.displayError = false;
      this.errorbutton =false;
      this.Errors=[];
    },
    uploadedGraph() {
      this.uploadingGraph = true;
      console.log(this.uploadingGraph);
    },
    //handleTopic takes in initial class data (topics, grade components, weights etc.)
    //takes uploaded file
    async handleTopicUpload(){
      this.uploading=true;
      this.uploadTopicsButton=false;
      //triggers overlay to be removed
      this.overlay();
      //uses filereader to read file contents, and convert them to a string
      this.file=this.$refs.file.files[0];
      const reader = new FileReader();
      reader.onload = event => console.log(event.target.result); // desired file content
      reader.onerror = error => reject(error);
      //this reads the text as a string
      reader.readAsText(this.file); // you could also read images and other binaries
      reader.onload = function(e,onComplete) {
        var stuff = reader.result;
        console.log(stuff);
        //removes commas from csv and newlines
        console.log('lmao, ',stuff.split(new RegExp('[' +'/, | /\n' + ']', 'g')));
        var separators=[' ', '↵'];
        var arrayOfString =stuff.split(new RegExp('[' +'/, | /\n' + ']', 'g'));
        var i =0;
        //currenttopic='';
        console.log('arrayofstring is currently: ',typeof arrayOfString);
        var arrayOfString = arrayOfString.filter(function (el) {
          return el != '';
        });
        //iterates through text looking for keywords.
        //create nodes first, then you can add edges
        for(i;i<arrayOfString.length;i++){
          if(arrayOfString[i]=='topicname'){
            this.tname =arrayOfString[i+1];
            i++;
            this.tid=Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 5);;//here
            let parentname=arrayOfString[i+1];
            this.createTopic();
          }
          if(arrayOfString[i]=='parentOf'){
            //if (newData.edges && newData.nodes) {
            //this.edge.ancestor_node=arrayOfString[i+1];
            //this.edge.topic_node = parentname;
            /*this.edges = newData.edges.map(edge => {
              return { from: arrayOfString[i+1], to: parentname, id: edge.pk };
            };*/
            //this.newdata.edges.to=arrayOfString[i];
            //this.newdata.edges.to=parentname;
            //this.nodes = this.generate_custom_graph_markup(newData.nodes);
            //this.options = options(this.layoutMethod);
            //}
            //nEdges[from] = tname;
            //nEdges[to] = tname;
            //stored in visdata
          }
        }
        this.saveEdits().then(()=>{
          this.getData(arrayOfString).then((data)=>{
            this.saveEdits();
          }).catch(()=>{
            this.Errors.push('Course creation failed');
            console.log('ERRORRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR , ',this.Errors);
            if((this.Errors.length)>0){
              console.log('TRIGGE(RING ERROR!!!');
              this.errorbutton=true;
            }
          });
        });
      }.bind(this);
        
    },
    async getData(arrayOfString){ // gets topics for the specific course
      let dat={};
      let nametoPK = {};
      let idtoPK = {};
      axios.get(`${API_URL}/topics/?courseId=${this.id}`)
        .then(data => {
          for(let x in data.data.result){
            this.nameto[data.data.result[x].name]=data.data.result[x].pk;
          }
        }).catch(() => {
          this.errorbutton=true;
          this.Errors.push('Course creation failed');
        }).finally(() => {
          //newstuff
          this.setupTopics(arrayOfString);
        });
    },
    async setupTopics(arrayOfString){
      let nametoPK=this.nameto;
      let storevals={};
      for( var key in Object.keys(nametoPK)){
      }
      let parent = '';
      let child='';
      let categoryData = {
        category: '',
        weight: 0,
        topic: 0
      };
      let i=0;
      for(i=0;i<arrayOfString.length;i++){
        if(arrayOfString[i]=='topicname'){
          parent = arrayOfString[i+1];
        }
        if(arrayOfString[i]=='category'){
          console.log('IN CATEGORY');
          categoryData.category= arrayOfString[i+1];
          categoryData.weight=(arrayOfString[i+2]);
          categoryData.topic = this.nameto[parent];
          // Post and create
          let newData= JSON.parse(JSON.stringify(categoryData));
          axios
            .post(`${API_URL}/topic/category/`, newData)
            .then(response => {})
            .catch(()=>{
              
              this.Errors.push(`Category error: ${parent}`);
              this.errorbutton=true;
              console.log('BROKEN',this.Errors.length, errorbutton);
            });
        }
          

        if(arrayOfString[i]==='parentOf'){
          child = arrayOfString[i+1];
          for(let x in this.$children[0].nodes){

            if(this.$children[0].nodes[x].topic.name===child){
              this.$children[0].nodes[x].id=this.nameto[child];
            }
            else if(this.$children[0].nodes[x].topic.name===parent){
              this.$children[0].nodes[x].id=this.nameto[parent];
            }
          }
          this.$children[0].visData.edges._data[(child+parent)] = {
            to: this.nameto[child],
            from:this.nameto[parent],
            id:((child+parent))
          };
          let newvals = {
            to: (this.nameto[child]),
            from: ( this.nameto[parent]),
            id:((child+parent)),
            parent:parent, child:child,
          };
          storevals[child+parent] = newvals;
                
                
        }
      }
      let PKVAL=nametoPK;
      this.saveEdges2(storevals,PKVAL);
            
    },


    //handle upload of grades for individual students

    async handleGradesUpload(){
      this.uploadGradesButton=false;
      this.uploading=true;
      this.overlay();
      this.file=this.$refs.file.files[0];
      const reader = new FileReader();
      reader.onload = event => console.log(event.target.result); // desired file content
      reader.onerror = error => reject(error);
      //this reads the text as a string
      reader.readAsText(this.file); // you could also read images and other binaries
      //readAsText is asynchronous so we have to wait for it ot be ready.
      reader.onload = function(e,onComplete) {
        var stuff = reader.result;
        //removes commas from csv and newlines
        var separators=[' ', '↵'];
        var arrayOfString =stuff.split(new RegExp('[' +'/, | /\n' + ']', 'g'));
        var i =0;
        //currenttopic='';
        var arrayOfString = arrayOfString.filter(function (el) {
          return el != '';
        });

        

            
        let Json={
          studentEmail : '',
          topicName : '',
          gradeVal : 0,
          name : '',
          category : '',
        };
        //
        console.log('gothere');
        for(i;i<arrayOfString.length;i++){
          if(i>4){
            if(i%5==0){
              console.log('FIRST: ',arrayOfString[i]);
              Json.studentEmail=arrayOfString[i];
            }
            if(i%5==1){
              console.log('FIRST: ',arrayOfString[i]);
              Json.topicName=arrayOfString[i];
            }else
            if(i%5==2){
              console.log('second: ',arrayOfString[i]);
              Json.name=arrayOfString[i];
            }else
            if(i%5==3){
              console.log('third: ',arrayOfString[i]);
              Json.category=arrayOfString[i];
            }else
            if(i%5==4){
              console.log('last: ',arrayOfString[i]);
              Json.gradeVal= parseInt(arrayOfString[i]);
              let newObject =JSON.parse(JSON.stringify(Json));
              console.log('JSON',newObject);
              this.getId(newObject).then((id)=>{
                console.log('NewObject' ,newObject);
              }).catch(()=>{
                this.Errors.push('Grade creation failed for ', Json.studentEmail, Json.topicName);
                this.errorbutton=true;
              });
            }
          }
          
        }
        console.log('ERRORRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR , ',this.Errors);//????
        if((this.Errors.length)>0){
          console.log('TRIGGERING ERROR!!!');
          this.errorbutton=true;
        }
        

      }.bind(this);
      
        
    },
    //get student ID from database
    async getId(Json){
      return new Promise((resolve, reject) => {
        let studentRoster= [];
        let final_id='noone';
        let done = false;
        axios
          .get(`${API_URL}/students/`)
          .then(response => {
            const students = response.data.result;
            studentRoster = students.filter((student, index) => {
              if({student}.student.email===Json.studentEmail && !done){
                let final_id={student}.student.pk;
                console.log('MAKINGGRADE');
                this.createGrade(final_id,Json);
                done=true;
              }
            });
          })
          .catch(() => {
            
          })
          .finally(() => {
            if(done===false){
              this.Errors.push('Grade not created for  '+Json.studentEmail+' ? '+Json.name);
              this.errorbutton=true;
              console.log('Grade not created for  '+Json.studentEmail+' ? '+Json.name);
            }
            done=false;
          });
      });
    
    },
    //Json holds the information to create a grade, create it for the student id.
    async createGrade(id_val,Json){
      const student_id = id_val;
      //console.log("");
      axios
      //get topics
        .get(`${API_URL}/student/topics/${this.id}/${student_id}`)
        .then(studentTopicData => {
          //console.log("topics");
          let doesTopicExist=false;
          for(let x in studentTopicData.data.result){
            console.log('EXISTS1? ',studentTopicData.data.result[x].topic.name, Json.topicName);
            if(studentTopicData.data.result[x].topic.name===Json.topicName){
              console.log('EXISTS2? ',studentTopicData.data.result[x].topic.name, Json.topicName);
              doesTopicExist=true;
              //create grade
              //get categories for the current course
              axios
                .get(`${API_URL}/topic/category/${studentTopicData.data.result[x].topic.id}/${Json.category}`)
                .then(topictocat => {                  let exists=false;
                  for(let x in topictocat.data.result){
                    console.log('EXISTS3? ',topictocat.data.result.category , Json.category, Json.topicName);

                    if(topictocat.data.result.category===Json.category){
                      
                      exists=true;
                      //putting grade category together
                      let newGrade={
                        'name': Json.name,
                        'student': id_val,
                        'value':Json.gradeVal,
                        'topic_to_category': topictocat.data.result.pk
                      };
                      //post newGrade to create grade information.
                      console.log('NEW GRADE BEING MADE? ', newGrade);
                      axios
                        .post(`${API_URL}/grades/`, newGrade)
                        .then(response => {})
                        .catch(()=> {
                          this.Errors.push('Grade not created for  '+Json.studentEmail+' ? '+Json.name);
                          console.log(error);
                        });
                      break;
                    }
                              
                  }
                 

                }).catch(()=>{
                  this.Errors.push('category not created for  '+Json.studentEmail+' ? '+Json.category);
                  this.errorbutton=true;
                });
              break;
            }
            if(!doesTopicExist){
              //this.Errors.push('This topic doesnt exist for '+Json.studentEmail+' ? '+ Json.topicName);
            }
            doesTopicExist=false;
          }
                  
        }).catch(()=> {
          this.Errors.push('Topic doesnt exist for  '+Json.studentEmail+' ? '+Json.topicName);
          this.errorbutton=true;
        });
    },
    Calling() {
      this.uploadButton = false;
      this.uploadGradesButton = false;
      this.uploadTopicsButton = false;
    },
    //saves just the edges
    async saveEdges2(newEdges,nametoPK) {
      let idtoPK = {};
      axios.get(`${API_URL}/topics/`)
        .then(data => {
          //map topic names to pk values and then id values to pk values.
          //old nodes ids and pk values are the same so it only really matters for the new ones
          let tops = data.data.result.filter((value, index, arr) => {
            return value.course == this.id;
          });
          // console.log(tops);
          let edgyPost = Array();
          this.nEdges = idtoPK;
          for(let x in newEdges){
            let top = newEdges[x]['to'];
            let anc = newEdges[x]['from'];
            let topc = newEdges[x]['child'];
            let ance = newEdges[x]['parent'];
            let topicToTopic = {
              topic_node: top,
              course: this.classData.uuid,
              ancestor_node: anc,
            };
            edgyPost.push(topicToTopic);
          }
           
          
          //Posts edges to DB
          axios
            .post(`${API_URL}/topic/topics/`, edgyPost)
            .then(data => {
              this.isSaved = true;
            })
            .catch(error => {
              this.errorbutton=true;
              this.Errors.push('Edge creation failed for one or more edges (make sure topic names are correct)');
              console.log(error);
            });
        }).catch(error=>{
          
        });
    },
    async saveEdges(newEdges) {
      let nametoPK = {};
      let idtoPK = {};
      axios
        .get(`${API_URL}/topics/`)
        .then(data => {
          //map topic names to pk values and then id values to pk values.
          //old nodes ids and pk values are the same so it only really matters for the new ones
          let tops = data.data.result.filter((value, index, arr) => {
            return value.course == this.id;
          });
          // console.log(tops);
          tops.forEach(topic => {
            nametoPK[topic.name] = topic.pk;
          });
          this.nodes.forEach(node => {
            if (nametoPK[node.topic.name] !== null) {
              idtoPK[node.id] = nametoPK[node.topic.name];
            }
          });
          let edgyPost = Array();
          this.nEdges = idtoPK;
          newEdges.forEach(edge => {
            let top = edge['to'];
            let anc = edge['from'];
            let topc = idtoPK[top];
            let ance = idtoPK[anc];
            let topicToTopic = {
              topic_node: topc,
              course: this.classData.uuid,
              ancestor_node: ance,
            };
            edgyPost.push(topicToTopic);
          });
          //Posts edges to DB
          axios
            .post(`${API_URL}/topic/topics/`, edgyPost)
            .then(data => {
              this.isSaved = true;
            })
            .catch(error => {
              console.log(error);
            });
        })
        .catch(error => {});
    },
    //saves everything
    saveEdits() {
      return new Promise((resolve, reject) => {
        console.log('DIANE');
        console.log('gothere');
        let newNodes = Array();
        let nEdges = this.$children[0].$data.visData.edges._data;
        //figure out which nodes arent saved
        this.nodes.forEach(node => {
          let tempTopic = node.topic;
          if (tempTopic.id === 'None') {
            newNodes.push({
              pk: 'None',
              course: tempTopic.course,
              name: tempTopic.name,
            });
            node.topic.id = 'saved';
          }
        });
        console.log('gothere2');
        console.log('edges?', this.nodes);
        // this.nEdges = nEdges;

        //converts bullshit edge storage object to JSON string then manually parse to usable form
        let parse = JSON.stringify(nEdges);
        console.log('nedges' ,JSON.stringify(nEdges));
        parse = parse.substring(1, parse.length - 2);
        let enu = parse.split('}');
        let tEdges = Array();
        while (enu.length > 0) {
          let g = enu.pop().split('{')[1];
          g = g.split(',');
          if (g.length > 2) {
            let from = g[0].split(':')[1];
            let to = g[1].split(':')[1];
            if(to.length>1){
              to = to.substr(1, to.length - 2);
            }
            if(from.length>1){
              from = from.substr(1, from.length - 2);
            }
            let id = g[2].split(':')[1];
            id = id.substring(1, id.length - 1);
            let ed = { from: from, to: to, id: id };
            tEdges.push(ed);
          }
        }

        //Determine which edges need saving
        let newEdges = Array();
        let cont = false;
        tEdges.forEach(tedge => {
          cont = false;
          this.edges.forEach(edge => {
            if (edge.id === tedge.id) {
              cont = true;
            }
          });
          if (!cont) {
            newEdges.push(tedge);
          }
        });


        let nametoPK = {};
        let idtoPK = {};
        // Post new topics to dB
        if(newNodes.length>0){
          axios
            .post(`${API_URL}/topics/`, newNodes)
            .then(data => {
              // retrieve posted topics to obtain pk values
              axios
                .get(`${API_URL}/topics/`)
                .then(data => {
                  //map topic names to pk values and then id values to pk values.
                  //old nodes ids and pk values are the same so it only really matters for the new ones
                  let tops = data.data.result.filter((value, index, arr) => {
                    return value.course == this.id;
                  });
                  tops.forEach(topic => {
                    nametoPK[topic.name] = topic.pk;
                  });
                  this.nodes.forEach(node => {
                    if (nametoPK[node.topic.name] !== null) {
                      idtoPK[node.id] = nametoPK[node.topic.name];
                    }
                  });
                  let newSTT = Array();

                  // Gather Teacher ID
                  axios
                    .get(`${API_URL}/students/?id_token=${this.profile.id_token}`)
                    .then(res => {
                      const student_id = res.data.result.pk;
                      newNodes.forEach(node => {
                        console.log(node.name);
                        // Associate the teacher to the class
                        let studenttoTopic = {
                          pk: 'None',
                          course: this.classData.uuid,
                          student: student_id,
                          topic: nametoPK[node.name],
                          grade: 0,
                          locked: false,
                        };
                        newSTT.push(studenttoTopic);
                      });
                      let edgyPost = Array();
                      this.nEdges = idtoPK;

                      //Post studenttotopics 
                      axios
                        .post(`${API_URL}/student/topics/`, {
                          student: student_id,
                          topics: newSTT,
                        })
                        .then(data => {
                          console.log(data);
                        })
                        .catch(error => {
                          console.log(error);
                          this.errorbutton=true;
                          this.Errors.push('Can\'t make topic ',newSTT, ' for ',this.profile.email);
                        });

                      //Map edge temp ids to pks
                      newEdges.forEach(edge => {
                        let top = edge['to'];
                        let anc = edge['from'];
                        let topc = idtoPK[top];
                        let ance = idtoPK[anc];
                        let topicToTopic = {
                          topic_node: topc,
                          course: this.classData.uuid,
                          ancestor_node: ance,
                        };
                        if (topc) {
                          edgyPost.push(topicToTopic);
                        }
                      });

                      // Actually Post edges
                      axios
                        .post(`${API_URL}/topic/topics/`, edgyPost)
                        .then(data => {
                          console.log(data);
                          console.log('TODDCHAVEZ');
                          resolve();
                          this.isSaved = true;
                        })
                        .catch(error => {
                          this.errorbutton=true;
                          this.Errors.push('Can\'t make edge between',ance, ' and ', topc ,' for ',this.profile.email);
                          console.log(error);
                        });
                    })
                    .catch(error => {
                      this.errorbutton=true;
                      this.Errors.push('Profile doesn\'t exist or isn\'t added to this course',this.profile.email);
                      console.log(error);
                    });
                })
                .catch(error => {
                  console.log(error);
                })
                .finally(() => {
                  this.$router.push({
                    name: 'Edit',
                    params: { id: this.classData.uuid },
                  });
                });
            })
            .finally(() => {
              // this.$router.push({
              //   name: 'Edit',
              //   params: { id: this.classData.uuid },
              // });
            });
        } 
        //If no new topics just save edges
        else if(newEdges.length>0){
          this.saveEdges(newEdges);
        }
        //this.inEdit=false
        //this.topicModalIsOpen = false
      });
    },
    //copied from editpopup
    createTopic(event) {
      const SVG = generate_svg();
      let nodeImage;
      let node = {'course':this.classData,'grade':0,'id':this.tid,'locked':false,'student':{},'topic':{'course':this.classData.uuid,'id':'None','name':this.tname}};
      nodeImage = generate_svg(SVG, node.topic.name, node.grade, node.locked);
      node.shape = 'image';
      node.image = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(nodeImage);
      this.tid += 'a';
      this.nodes.push(node);
      this.tname = '';
      this.$emit('onClose');
    },  
    //similar to handleTopic, but for grades
    //not working yet (obviously)
    overlay(){
      this.inEdit=!this.inEdit;
      let el = document.getElementById('overlay');
      el.style.visibility = (el.style.visibility == 'visible') ? 'hidden' : 'visible';
    },
    CallingTopic(){
      this.uploadTopicsButton=!this.uploadTopicsButton;
      console.log('UPLOADBUTTON');
    },
    CallingGrade(){
      this.uploadGradesButton=!this.uploadGradesButton;
      console.log('UPLOADBUTTON');
  
     
    },
  },
  //this is an attempt to make a node
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
  watch: {
    data(newData) {
      // runs when data prop is updated
      if (newData.edges && newData.nodes) {
        this.edges = newData.edges.map(edge => {
          return { from: edge.ancestor_node, to: edge.topic_node, id: edge.pk };
        });
        this.nodes = this.generate_custom_graph_markup(newData.nodes);
        this.options = options(this.layoutMethod);
      }
    },
  },
};
</script>

<style>
.class-graph {
  height: 100%;
  position: relative;
}
.edit-class-graph {
  max-height: 81vh !important;
}
.network {
  height: 100%;
}
.edit.actions {
  margin-top: 8pt;
}
#create {
  position: fixed; /* Sit on top of the page content */
  display: none; /* Hidden by default */
  width: 100%; /* Full width (cover the whole page) */
  height: 100%; /* Full height (cover the whole page) */
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5); /* Black background with opacity */
  z-index: 2; /* Specify a stack order in case you're using a different order for other elements */
  cursor: pointer; /* Add a pointer on hover */
}
#overlay {
  visibility: hidden;
  position: absolute;
  left: 0px;
  top: 0px;
  width:100%;
  height:100%;
  text-align:center;
  z-index: 1000;
}
#overlay div {
    font-size: 20px;
    background-color: #fff;
    -webkit-box-shadow: 0 1px 2px 0 rgba(34,36,38,.15);
    box-shadow: 0 1px 2px 0 rgba(34,36,38,.15);
    border: 1px solid rgba(34,36,38,.15);
    padding: 30px;
    border-radius: 8px;
}
  .class-graph {
    height: 100%;
    position: relative;
  }
  .edit-class-graph { 
    max-height: 81vh !important;
  }
  .network {
    height: 100%;
    width: 100%;
    margin-left:auto;
    margin-right:auto;
}
.top {
  position:relative; 
  top: 40px;
}
.bottom {
  position:relative; 
  top: 120px;
}


</style>

