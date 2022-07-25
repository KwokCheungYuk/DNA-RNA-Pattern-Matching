<template>
  <div v-title data-title="DNA/RNA Pattern Matching" id="pattern_matching">
    <h1 id="title">DNA/RNA Pattern Matching</h1>
    <el-row :gutter="20">
      <el-col :span="8">
        <div class="grid-content bg-purple" id="sequence_container">
          <h2 class="container_description">DNA/RNA Sequences</h2>
          <div id="all_sequence">
            <div class="item_div"
                 v-for="(item, index) in sequence_list"
                 v-bind:key="index"
                 v-bind:id="'sequence_div' + index">
              <el-input
                class="item_name"
                :id="'sequence_name' + index"
                :placeholder="'Please enter Sequence' + (index + 1) + ' name'"
                prefix-icon="el-icon-edit"
                v-model="sequence_name[index]"
                clearable>
              </el-input>
              <el-input
                class="sequence"
                :id="'sequence' + index"
                v-model="sequence_list[index]"
                placeholder="Please enter DNA/RNA sequence. E.g ATCGATT"
                @input="checkInput(index, 'sequence')"
                clearable>
              </el-input>
              <div :id="'sequence_warning' + index" class="warning">
              This field can not be empty.
              </div>
            </div>
          </div>
          <div class="btn_div">
            <el-button
              type="danger"
              round
              id="delete_sequence_btn"
              class="delete_btn"
              :disabled="sequence_count===0"
              @click="deleteSequence()">
              Delete the last sequence
            </el-button>
          </div>
          <div class="btn_div">
            <el-button
              type="primary"
              round
              id="add_sequence_btn"
              class="add_btn"
              @click="addSequence()">
              Add a new sequence
            </el-button>
          </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="grid-content bg-purple" id="pattern_container">
          <h2 class="container_description">Patterns</h2>
          <div id="all_pattern">
            <div class="item_div"
                 v-for="(item, index) in pattern_list"
                 v-bind:key="index"
                 v-bind:id="'pattern_div' + index">
              <el-input
                class="item_name"
                :id="'pattern_name' + index"
                :placeholder="'Please enter Pattern' + (index + 1) + ' name'"
                prefix-icon="el-icon-edit"
                v-model="pattern_name[index]"
                clearable>
              </el-input>
              <el-input
                class="sequence"
                :id="'pattern' + index"
                v-model="pattern_list[index]"
                placeholder="Please enter pattern. E.g AAGG"
                @input="checkInput(index, 'pattern')"
                clearable>
              </el-input>
              <div :id="'pattern_warning' + index" class="warning">
              This field can not be empty.
              </div>
            </div>
          </div>
          <div class="btn_div">
            <el-button
              type="danger"
              round
              id="delete_pattern_btn"
              class="delete_btn"
              :disabled="pattern_count===0"
              @click="deletePattern()">
              Delete the last pattern
            </el-button>
          </div>
          <div class="btn_div">
            <el-button
              type="primary"
              round
              id="add_pattern_btn"
              class="add_btn"
              @click="addPattern()">
              Add a new pattern
            </el-button>
          </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="grid-content bg-purple" id="result_container">
          <h2 class="container_description">Matching Results</h2>
          <img id="waiting_img" src="../assets/waiting.gif" :hidden="has_result">
          <h3 :hidden="has_result">Waiting for processing......</h3>
          <div id="results_div" :hidden="!has_result">
            <div class="item_div"
                 v-for="(item, index) in result_list"
                 v-bind:key="index"
                 v-bind:id="'result_div' + index">
              <div :id="'result_title' + index" class="result_title"></div>
              <div :id="'result_content' + index" class="result_content">
              This field can not be empty.
              </div>
            </div>
            <el-button
              type="primary"
              round
              id="download_btn"
              class="add_btn"
              @click="download()">
              Download the results
            </el-button>
          </div>
        </div>
      </el-col>
    </el-row>
    <div class="btn_div">
      <el-button
        type="primary"
        round
        id="process_btn"
        @click="process()"
        :disabled="disable_process">
        Process
      </el-button>
    </div>
  </div>

</template>

<style>
  .bg-purple {
    background: #d3dce6;
  }

  .grid-content {
    border-radius: 15px;
    min-height: 36px;
    padding-top: 1px;
    text-align: center;
  }
  .el-button {
    width: 60%;
    margin-top: 10px;
  }

</style>

<style scoped>
  #pattern_matching {
    position: fixed;
    width: 100%;
    height: 100%;
    background-color: rgba(193, 193, 193, 0.7);
    overflow: scroll;
  }

  #title {
    color: #296fff;
  }

  .item_div {
    width: 95%;
    display: inline-block;
    background-color: #b4d8ff;
    padding-top: 10px;
    padding-bottom: 10px;
    border-radius: 10px;
    margin-bottom: 15px;
    overflow: hidden;
  }

  .item_name {
    width: 100%;
    position: relative;
    top: -10px;
  }

  .item_name /deep/ .el-input__inner{
    font-size: 16px;
    font-weight: bold;
  }

  .sequence{
    width: 95%;
  }

  .warning{
    margin: 5px;
    padding-left: 10px;
    color: red;
    font-size: 15px;
    text-align: left;
  }

  .add_btn{
    margin-bottom: 20px;
  }

  #process_btn{
    margin-top: 50px;
    width: 500px;
  }

  #waiting_img{
    width: 150px;
    height: 150px;
  }

  #results_div{
    width: 100%;
  }

  .result_title{
    padding-left: 5px;
    font-size: 20px;
    font-weight: bold;
    text-align: left;
  }

  .result_content{
    margin: 5px;
    padding-left: 1px;
    color: indianred;
    font-weight: bold;
    font-size: 15px;
    text-align: left;
  }
</style>

<script>

import axios from 'axios'
/*
Check whether string is valid
return code: 0 represents OK
             1 represents containing other invalid letters
             2 represents missing one side of []
             3 represents string contains both T and U
             4 represents empty string
             5 The content in [] is empty
             6 The content in [] just contains one character
             7 The content in [] is invalid
 */
function checkString (str) {
  let leftBracket = []
  let leftIndex = []
  let rightIndex = []
  // T and U exist at the same time
  if (str.indexOf('T') !== -1 && str.indexOf('U') !== -1) {
    return 3
  }
  // Nothing is entered
  if (str.length === 0) {
    return 4
  }
  // check the string
  for (let i = 0; i < str.length; i++) {
    // check characters
    if (str[i] !== 'A' && str[i] !== 'T' && str[i] !== 'C' && str[i] !== 'G' && str[i] !== 'U' && str[i] !== '[' && str[i] !== ']') {
      return 1
    }
    // check bracket
    if (str[i] === '[') {
      if (i + 1 < str.length && str[i + 1] === ']') {
        return 5
      }
      leftBracket.push('[')
      leftIndex.push(i)
    } else if (str[i] === ']') {
      if (leftBracket.length === 0) {
        return 2
      } else {
        leftBracket.pop()
        rightIndex.push(i)
      }
    }
    // only one character inside the bracket
    if (str[i] === '[' && i + 2 < str.length && str[i + 2] === ']') {
      return 6
    }
  }
  // check the contents in brackets
  for (let i = 0; i < leftIndex.length; i++) {
    let substr = str.substring(leftIndex[i] + 1, rightIndex[i])
    let chars = new Set()
    for (let j = 0; j < substr.length; j++) {
      if (chars.has(substr[j]) === true) {
        return 7
      } else {
        chars.add(substr[j])
      }
    }
  }
  if (leftBracket.length !== 0) {
    return 2
  }
  return 0
}

/*
Check whether all string is valid
if yes, return true, else return false
 */
function checkValidStatus (sequenceValid, patternValid) {
  if (sequenceValid.length === 0 || patternValid.length === 0) {
    return false
  }
  for (let i = 0; i < sequenceValid.length; i++) {
    if (sequenceValid[i] === false) {
      return false
    }
  }
  for (let i = 0; i < patternValid.length; i++) {
    if (patternValid[i] === false) {
      return false
    }
  }
  return true
}

export default {
  name: 'matching',
  data () {
    return {
      sequence_count: 0, // the number of sequence
      pattern_count: 0, // the number of pattern
      sequence_name: [], // to store each sequence's name
      pattern_name: [], // to store each pattern's name
      result_name: [], // to store each result's name
      sequence_list: [], // to store all sequences
      pattern_list: [], // to store all patterns
      result_list: [], // to store all matching result
      sequence_valid: [], // to store a boolean value for whether each sequence is valid
      pattern_valid: [], // to store a boolean value for whether each sequence is valid
      has_result: false, // whether matching results is obtained
      disable_process: true, // to control the process button
      result_sequence_list: [] // to store the result in original sequences
    }
  },
  methods: {
    deleteSequence () {
      this.sequence_count--
      // Find the last sequence element
      let toDeleteDiv = document.getElementById('sequence_div' + this.sequence_count)
      if (toDeleteDiv != null) {
        // Delete itself by finding the element's parent node
        toDeleteDiv.parentNode.removeChild(toDeleteDiv)
        // Pop up the data associated with the element
        this.sequence_name.pop()
        this.sequence_list.pop()
        this.sequence_valid.pop()
        this.has_result = false
        for (let i = 0; i < this.pattern_count; i++) {
          this.result_list.pop()
        }
        this.disable_process = !checkValidStatus(this.sequence_valid, this.pattern_valid)
      }
    },
    addSequence () {
      this.sequence_count += 1
      this.sequence_name.push('Sequence' + this.sequence_count)
      this.sequence_list.push('')
      this.sequence_valid.push(false)
      this.has_result = false
      for (let i = 0; i < this.pattern_count; i++) {
        this.result_list.push([])
      }
      this.disable_process = !checkValidStatus(this.sequence_valid, this.pattern_valid)
    },
    deletePattern () {
      this.pattern_count--
      // Find the last sequence element
      let toDeleteDiv = document.getElementById('pattern_div' + this.pattern_count)
      if (toDeleteDiv != null) {
        // Delete itself by finding the element's parent node
        toDeleteDiv.parentNode.removeChild(toDeleteDiv)
        // Pop up the data associated with the element
        this.pattern_name.pop()
        this.pattern_list.pop()
        this.pattern_valid.pop()
        this.has_result = false
        for (let i = 0; i < this.sequence_count; i++) {
          this.result_list.pop()
        }
        this.disable_process = !checkValidStatus(this.sequence_valid, this.pattern_valid)
      }
    },
    addPattern () {
      this.pattern_count += 1
      this.pattern_name.push('Pattern' + this.pattern_count)
      this.pattern_list.push('')
      this.pattern_valid.push(false)
      this.has_result = false
      for (let i = 0; i < this.sequence_count; i++) {
        this.result_list.push([])
      }
      this.disable_process = !checkValidStatus(this.sequence_valid, this.pattern_valid)
    },
    // Check whether the corresponding sequence or pattern is valid
    checkInput (index, type) {
      let inputValue = ''
      if (type === 'sequence') {
        inputValue = this.sequence_list[index]
      } else if (type === 'pattern') {
        inputValue = this.pattern_list[index]
      }
      let warningElement = document.getElementById(type + '_warning' + index)
      switch (checkString(inputValue)) {
        case 0:
          warningElement.innerHTML = ''
          if (type === 'sequence') {
            this.sequence_valid[index] = true
          } else if (type === 'pattern') {
            this.pattern_valid[index] = true
          }
          break
        case 1:
          warningElement.innerHTML = 'The sequence can only contain \'A\', \'T\', \'C\', \'G\', \'U\' and \'[]\'.'
          if (type === 'sequence') {
            this.sequence_valid[index] = false
          } else if (type === 'pattern') {
            this.pattern_valid[index] = false
          }
          break
        case 2:
          warningElement.innerHTML = 'Missing one side of the [].'
          if (type === 'sequence') {
            this.sequence_valid[index] = false
          } else if (type === 'pattern') {
            this.pattern_valid[index] = false
          }
          break
        case 3:
          warningElement.innerHTML = 'T and U can not appear at the same time.'
          if (type === 'sequence') {
            this.sequence_valid[index] = false
          } else if (type === 'pattern') {
            this.pattern_valid[index] = false
          }
          break
        case 4:
          warningElement.innerHTML = 'This field can not be empty.'
          if (type === 'sequence') {
            this.sequence_valid[index] = false
          } else if (type === 'pattern') {
            this.pattern_valid[index] = false
          }
          break
        case 5:
          warningElement.innerHTML = 'The contents in brackets cannot be empty.'
          if (type === 'sequence') {
            this.sequence_valid[index] = false
          } else if (type === 'pattern') {
            this.pattern_valid[index] = false
          }
          break
        case 6:
          warningElement.innerHTML = 'The contents in brackets cannot just contain one character.'
          if (type === 'sequence') {
            this.sequence_valid[index] = false
          } else if (type === 'pattern') {
            this.pattern_valid[index] = false
          }
          break
        case 7:
          warningElement.innerHTML = 'The contents in some brackets are not valid.'
          if (type === 'sequence') {
            this.sequence_valid[index] = false
          } else if (type === 'pattern') {
            this.pattern_valid[index] = false
          }
          break
        default:
          warningElement.innerHTML = 'Something unexpected has happened.'
          if (type === 'sequence') {
            this.sequence_valid[index] = false
          } else if (type === 'pattern') {
            this.pattern_valid[index] = false
          }
          break
      }
      this.disable_process = !checkValidStatus(this.sequence_valid, this.pattern_valid)
    },
    // Upload data to back end and display the result
    process () {
      let loading = this.$loading({
        lock: true,
        text: 'Processing in backend, please wait......',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      })
      const path = 'http://127.0.0.1:5000/matching'
      // const path = 'http://3.208.12.12:5000/matching'
      // create Form object
      let uploadData = new FormData()
      for (let i = 0; i < this.sequence_list.length; i++) {
        uploadData.append('sequences', this.sequence_list[i])
      }
      for (let i = 0; i < this.pattern_list.length; i++) {
        uploadData.append('patterns', this.pattern_list[i])
      }
      let config = {
        headers: {'Content-Type': 'multipart/form-data'}
      }
      axios.post(path, uploadData, config)
        .then((res) => {
          loading.close()
          if (res.data['result_index'].length !== this.sequence_count * this.pattern_count) {
            this.$notify.error({
              title: 'ERROR',
              message: 'Something wrong! Please try again!'
            })
            this.result_list = []
            this.has_result = false
          } else {
            // Something wrong if I use this statement to copy values. The titleElement will become null
            // this.result_list = res.data['result_index']
            for (let i = 0; i < res.data['result_index'].length; i++) {
              this.result_list[i] = res.data['result_index'][i]
            }
            this.result_sequence_list = res.data['result_sequence']
            for (let i = 0; i < this.sequence_count; i++) {
              for (let j = 0; j < this.pattern_count; j++) {
                let actualIndex = i * this.pattern_count + j
                let titleElement = document.getElementById('result_title' + actualIndex)
                let contentElement = document.getElementById('result_content' + actualIndex)
                titleElement.innerHTML = this.sequence_name[i] + ' and ' + this.pattern_name[j]
                if (this.result_list[actualIndex][0] === -1) {
                  contentElement.innerHTML = 'There is no occurrence.'
                } else if (this.result_list[actualIndex][0] === -2) {
                  contentElement.innerHTML = 'Sequence and Pattern can not both be degenerate string.'
                } else {
                  if (this.result_list[actualIndex].length === 1) {
                    contentElement.innerHTML = 'There is 1 occurrence, starting at position ' + this.result_list[actualIndex][0] + '.'
                  } else {
                    contentElement.innerHTML = 'There are ' + this.result_list[actualIndex].length + ' occurrences, starting at positions '
                    for (let k = 0; k < this.result_list[actualIndex].length - 1; k++) {
                      contentElement.innerHTML += this.result_list[actualIndex][k] + ', '
                    }
                    contentElement.innerHTML += 'and ' + this.result_list[actualIndex][this.result_list[actualIndex].length - 1] + '.'
                  }
                }
              }
            }
            this.disable_process = true
            this.has_result = true
          }
        })
        .catch((error) => {
          loading.close()
          console.error(error)
          this.$notify.error({
            title: 'Network Error',
            message: 'Something wrong! Please try again!'
          })
        })
    },
    download () {
      let titleList = document.getElementsByClassName('result_title')
      let contentList = document.getElementsByClassName('result_content')
      let downloadData = ''
      for (let i = 0; i < this.sequence_count; i++) {
        for (let j = 0; j < this.pattern_count; j++) {
          let actualIndex = i * this.pattern_count + j
          downloadData += titleList[actualIndex].innerHTML + '\n'
          downloadData += 'Sequence: ' + this.sequence_list[i] + '\n'
          downloadData += 'Pattern: ' + this.pattern_list[j] + '\n'
          downloadData += 'Result: ' + contentList[actualIndex].innerHTML + '\n'
          if (this.result_list[actualIndex][0] !== -1 && this.result_list[actualIndex][0] !== -2) {
            downloadData += 'The matching result in original sequence: ' + this.result_sequence_list[actualIndex] + '\n\n'
          } else {
            downloadData += '\n'
          }
        }
      }
      let blob = new Blob([downloadData], {type: 'text/latex'})
      let url = window.URL.createObjectURL(blob)
      let a = document.createElement('a')
      a.href = url
      a.download = 'Matching Result.txt'
      a.click()
      window.URL.revokeObjectURL(url)
    }

  }
}
</script>
