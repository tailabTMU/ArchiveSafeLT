# ACSAC22-Artifacts

Paper: Sabry, Moe, and Reza Samavi. "ArchiveSafe LT: Secure Long-term Archiving System." Proceedings of the 38th Annual Computer Security Applications Conference (ACSAC). 2022.
Slides: https://www.acsac.org/2022/program/papers/128-sabry-resilience_and_data_protection.pdf
ArchiveSafe LT ACSAC '22 Artifacts

The artifacts are divided into three groups:
 - Experiment Code: Contains the code used to run the evaluation experiment detailed in Section 5. The code is written in Python.
 - Data Results: Contains the data points collected by the evaluation experiment and presented in Section 5.
 - Tamarin Files: Contains the Tamarin theory files modeling the security experiments for the design detailed in Section 4.3. 

Experiment Code:
 - CreateSample.py: A Python program used to generate random data files to be used as sample archive files in the evaluation experiment. It generates groups of files in different data sizes. 
 - RunFileExp.py: A Python program simulating an update of a leaf in the Merkle tree. This event corresponds to an update to the contents of an archive file. The program measures the time needed to update a leaf in a tree using different size trees.
 - RunConfExp.py: A Python program used to measure the time needed to evolve the confidentiality of archives of different sizes. The program uses the sample files created by the CreateSample.py application. It performs the initial creation of the archive followed by three evolution processes. The program measures the time needed for the initial creation of the archive and the subsequent evolution processes.
 - RunIntExp.py: A Python application used to measure the time needed to evolve the integrity of archives of different sizes. The program uses the encrypted files created by the RunConfExp.py application. It measures the time needed to evolve the integrity of archives of different sizes.

Data Results:
 - Archive Confidentiality Exp.xlsx: The data points collected by the RunConfExp.py program.
 - Archive Integrity Exp.xlsx: The data points collected by the RunIntExp.py program.
 - Tree Update:  The data points collected by the RunFileExp.py program.

Tamarin Files:
In order to run these files, Tamarin Automatic Prover must be installed (http://tamarin-prover.github.io/). To run a file, run "tamarin-prover interactive example.spthy" on the comand prompt then go to "http://127.0.0.1:3001" from the browser.
 - archivelt_conf.spthy: A Tamarin theory file simulating the confidentiality experiment.
 - archivelt_forge.spthy: A Tamarin theory file simulating the integrity experiment.



# Running the Experiment
The experiment has three phases to be run in sequence: 
A. Create the required subdirectories.
B. Run the confidentiality experiment.
C. Run the integrity experiment.
D. Run the tree size experiment.

A. Steps to create the required subdirectories:
In the directory where the experiment will be run:
1. Run "mkdir sample".
2. Run "mkdir Initial".
3. Run "mkdir InitialRet".
4. Run "mkdir FirstEvol".
5. Run "mkdir FirstRet".
6. Run "mkdir SecondEvol".
7. Run "mkdir SecondRet".
8. Run "mkdir ThirdEvol".
9. Run "mkdir ThirdRet".

B. Steps to run the confidentiality experiment:
1. Create sample files: Run "python3 CreateSample.py". Creates sample files to be used in the experiment. It creates the files in a subdirectory named "/sample" under the current directory.
2. Run the confidentiality experiment: "python3 RunConfExp.py". This program performs multiple steps:
 a. Creates initial archives from the sample files created in step 1. The sample files are double encrypted and integrity Merkle trees created. The output files are stored in a subdirectory "/Initial".
 b. Retrieve the archive to its plain data form. Read files from "/Initial" and retrieve the files to "/InitialRet".
 c. Perform the first evolution on the archive files. Evolve the archive files by renecrypting them again and recalculates the integrity Merkle trees. Read the files from the "/Initial" subdirectory and write the evolved files in the "/FirstEvol" subdirectory.
 d. Retrieve the archive to its plain data form. Read files from "/FirstEvol" and retrieve the files to "/FirstRet".
 e. Perform the second evolution on the archive files. Evolve the archive files by renecrypting them again and recalculates the integrity Merkle trees. Read the files from the "/FirstEvol" subdirectory and write the evolved files in the "/SecondEvol" subdirectory.
 f. Retrieve the archive to its plain data form. Read files from "/SecondEvol" and retrieve the files to "/SecondRet".
 e. Perform the third evolution on the archive files. Evolve the archive files by renecrypting them again and recalculates the integrity Merkle trees. Read the files from the "/SecondEvol" subdirectory and write the evolved files in the "/ThirdEvol" subdirectory.
 f. Retrieve the archive to its plain data form. Read files from "/ThirdEvol" and retrieve the files to "/ThirdRet".
3. Record the times for all the operations in the 'Report.txt'

C. Steps to run the integrity experiment:
1. Keeps all files and subfolders created during the confidentiality experiment.
2. Run "python3 RunIntExp.py"
3. Results are stored in 'Integrity Evolution Report.txt'

D. Steps to run the tree size experiment:
1. Run "python3 RunFileExp.py".
2. Results are stored in the 'Report.txt'.

# Cite
If you find the content useful for your research and applications, please cite us using this BibTeX:

```bibtex
@inproceedings{10.1145/3564625.3564635,
    author = {Sabry, Moe and Samavi, Reza},
    title = {ArchiveSafe LT: Secure Long-term Archiving System},
    year = {2022},
    isbn = {9781450397599},
    publisher = {Association for Computing Machinery},
    address = {New York, NY, USA},
    url = {https://doi.org/10.1145/3564625.3564635},
    doi = {10.1145/3564625.3564635},
    abstract = {Every year the amount of digitally stored sensitive information increases significantly. Information such as governmental and legal documents, health, and tax records are required to be securely archived for decades to comply with various laws and regulations. Since cryptographic schemes based on single computational assumptions are not guaranteed to stay secure for such long periods, current state-of-the-art systems providing long-term confidentiality and integrity rely on information-theoretic techniques, such as multi-server secret sharing and commitments. These systems achieve the desired results; however, establishing private channels for secret sharing is costly and requires a complex setup. In this paper, we present ArchiveSafe LT, a framework for archiving systems aiming to provide long-term confidentiality and integrity. The framework relies on multiple computationally-secure schemes using robust combiners, with a design that plans for agility and evolution of cryptographic schemes. ArchiveSafe LT is efficient and suitable for practical adoption as it eliminates the need for private channels compared to its counterparts. We present the ArchiveSafe LT framework structure and its security analysis using an automatic prover. We specify two ArchiveSafe LT-based system designs, which handle different adversarial storage providers. We experimentally evaluate a prototype built based on one of the designs to show the system’s efficiency compared to information-theoretic systems.},
    booktitle = {Proceedings of the 38th Annual Computer Security Applications Conference},
    pages = {936–948},
    numpages = {13},
    keywords = {Long-term Archiving, Long-term Confidentiality, Long-term Integrity, Secure Cloud Storage},
    location = {Austin, TX, USA},
    series = {ACSAC '22}
}
```