# Bean Theory
## a unified webpage for Number Theory seminars in the Boston area

https://beantheory.org



# Installing
### Clone the repository
```
git clone git@github.com:edgarcosta/beantheory.git
```
or
```
git clone https://github.com/edgarcosta/beantheory.git
```

### Install dependencies
```
pip install -r requirements.txt
```

# Adding a special seminar

Edit (beantheory/seminars/special.yaml)[https://github.com/edgarcosta/beantheory/blob/master/beantheory/seminars/special.yaml] accordingly and submit your changes with a PR.
The next time the data is generated new special seminar will be included.

# Generating new data

The data for the website is generated every day 6am EST with:
```
python generate-data.py
```

# Coverage

- BU Number Theory: http://math.bu.edu/research/algebra/seminar.html
- MIT Number Theory: http://math.mit.edu/nt/nts.html
- BC-MIT joint: https://www2.bc.edu/benjamin-howard/BC-MIT.html
- BC NT &AG seminar: https://sites.google.com/bc.edu/seminar2018-19/home
- Tufts AGeNTS: https://sites.google.com/view/tuftsagents/home
- Harvard's: http://www.math.harvard.edu/cgi-bin/showtalk.pl 
- MIT STAGE: http://math.mit.edu/nt/index_stage.html
- special seminars by request

