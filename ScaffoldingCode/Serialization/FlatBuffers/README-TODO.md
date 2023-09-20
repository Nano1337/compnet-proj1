## Follow README.md for installation instructions. 
Also do a quick 'pip install flatbuffers'. 

### Instructions for Lily: 
- Modify 'schema.fbs' according to the instructions/comments
- Validate that our schema meets all required elements as specified in the instructions
- Compile with 'flatc --python schema.fbs' on the command line
- Push changes to github

### Instructions for Rob: 
- Modify the following files to incorporate the new elements from schema that Lily has added
  - 'serializers.py'
  - 'custom_msg.py'
  - 'flatbufdemo_local.py'
- Fix all the parts labeled FIXME in each file, should be in same format as ORDERS, which already works.
- Write up quick report as directed by instructions and submit to brightspace

