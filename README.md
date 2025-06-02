# Job Screening AI

Job Screening AI is an application designed to streamline the recruitment process by automating the screening of job descriptions and CVs. This project utilizes various components to summarize job descriptions, parse CVs, score matches, shortlist candidates, and manage interview scheduling.

## 📽 Demo Video

[![Watch the demo](https://img.youtube.com/vi/VIDEO_ID/0.jpg)](https://drive.google.com/file/d/1IJLotoC_0fqF-o3l6zljoXCavMkHJXpZ/view?usp=drivesdk)

## Components

- **Agents**: 
  - `jd_summarizer.py`: Summarizes job descriptions and extracts key responsibilities and qualifications.
  - `cv_parser.py`: Parses CVs to extract relevant information such as work experience and education.
  - `match_scorer.py`: Scores the match between job descriptions and CVs based on various criteria.
  - `shortlister.py`: Shortlists candidates based on scores from the `MatchScorer`.
  - `scheduler.py`: Manages interview scheduling and times.

- **Data**:
  - `sample_jd.txt`: Contains a sample job description in plain text format.
  - `sample_cv.pdf`: Contains a sample CV in PDF format.


## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd job_screening_ai
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/app.py
```

This will initialize the job screening process and coordinate between the various components of the application.

