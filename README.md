makes for a quick templating job when taking your first run at form forming.

in this very early version there are outstanding issues, namely that there are no attempts made at generating unique ids for any part of the form. because of this, the initial file it generates could potentially be used to create new instances of the form by just re-re-re-re-reimporting it. for that reason the file should be imported first, then confirmed for functionality, then export the confirmed functional version of the form and leave the other one alooooone.

eventual goal is to load the actual file and create an XML/FML doc from it which can be edited without losing those sweet delicious uuids. in this way an existing form file could be edited and then re-imported without breaking data ties.