%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Minimal Memorandum
% LaTeX Class
% Version 1.0 (March 3, 2022)
%
% This class originates from:
% https://www.LaTeXTemplates.com
%
% Author:
% Vel (vel@latextemplates.com)
%
% License:
% CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/)
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%----------------------------------------------------------------------------------------
%	CLASS CONFIGURATION
%----------------------------------------------------------------------------------------

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{CSMinimalMemo}[2022/03/03 Creodocs Minimal Memo Class v1.0]

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}} % Pass through any extra options specified to the base class
\ProcessOptions\relax % Process class options

\LoadClass{article} % Load the base class

%----------------------------------------------------------------------------------------
%	PACKAGES AND OTHER DOCUMENT CONFIGURATIONS
%----------------------------------------------------------------------------------------

\usepackage{setspace} % Required for changing line spacing

\usepackage{etoolbox} % Required for conditional logic and easily changing commands

\usepackage[hidelinks]{hyperref} % Required for links

\usepackage{graphicx} % Required for including images

\setlength{\parindent}{0pt} % Stop paragraph indentation
\setlength{\parskip}{\baselineskip} % Vertical whitespace between paragraphs

\raggedright % Suppress justification

%----------------------------------------------------------------------------------------
%	MARGINS
%----------------------------------------------------------------------------------------

\usepackage{geometry} % Required for adjusting page dimensions and margins

\geometry{
	top=2.5cm, % Top margin
	bottom=5cm, % Bottom margin
	left=2cm, % Left margin
	right=2cm, % Right margin
	footskip=1.75cm, % Space from the bottom margin to the baseline of the footer
	%showframe, % Uncomment to show how the type block is set on the page
}

%---------------------------------------------------------------------------------
%	FONTS
%---------------------------------------------------------------------------------

\usepackage[utf8]{inputenc} % Required for inputting international characters
\usepackage[T1]{fontenc} % Output font encoding for international characters

\usepackage[default]{lato} % Use the Lato sans serif font

%----------------------------------------------------------------------------------------
%	HEADERS AND FOOTERS
%----------------------------------------------------------------------------------------

\usepackage{fancyhdr} % Required for customizing headers and footers
\pagestyle{fancy} % Enable custom headers and footers

\renewcommand{\headrulewidth}{0pt} % Top horizontal rule thickness

\fancyhf{} % Clear default headers/footers

\fancyfoot[L]{ % Left footer
	% Use separate tables so Creodocs can easily add lines to each block
	\begin{memocontactinfotable}
		\leftcontactinfo
	\end{memocontactinfotable}%
	\hspace{0.04\textwidth}% Horizontal whitespace between tables
	\begin{memocontactinfotable}
		\centercontactinfo
	\end{memocontactinfotable}%
	\hspace{0.04\textwidth}% Horizontal whitespace between tables
	\begin{memocontactinfotable}
		\rightcontactinfo
	\end{memocontactinfotable}%
}

%----------------------------------------------------------------------------------------
%	TABLES
%----------------------------------------------------------------------------------------

\usepackage{array} % Required for manipulating table columns

\newcolumntype{R}[1]{>{\raggedleft\arraybackslash}p{#1}} % Define a new right-aligned paragraph column type
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}} % Define a new left-aligned (no justification) paragraph column type
\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}} % Define a new centered paragraph column type

%---------------------------------------------------------------------------------
%	HEADER
%---------------------------------------------------------------------------------

\newcommand{\outputheader}{ % Command to output the header using information entered by the user
	\setstretch{1.2} % Increase line spacing in the header
	
	{\Huge\MakeUppercase{\memotitle}} % Document title
	
	\ifstrempty{\memodate}{}{{\large\memodate}} % Memo date (optional)
	
	\vspace{0.05\textheight} % Vertical whitespace
	
	%------------------------------------------------
	
	\begingroup
		\large % Increase font size inside the table
		\begin{tabular}{@{} l L{0.7\textwidth} @{}} % 2 columns, one with an automatic width and the other fixed-width
			\memoinfotable % Add the table rows specified in the template
		\end{tabular}
	\endgroup
	
	\vspace{0.06\textheight} % Vertical whitespace

	\setstretch{1} % Restore single line spacing
}

\newcommand{\memoinfotablerow}[2]{\textbf{#1} & #2\\} % Command to output each row of the memo information table

%---------------------------------------------------------------------------------
%	MEMO CONTACT INFORMATION TABLES
%---------------------------------------------------------------------------------

\newenvironment{memocontactinfotable}{
	\begin{tabular}[t]{@{} L{0.29\textwidth} @{}}% Single column with a left-aligned fixed width with no padding around it. The table is top-aligned so unequal numbers of rows in the tables look neat next to each other.
}{
	\end{tabular}
}

%----------------------------------------------------------------------------------------
%	CUSTOM COMMANDS
%----------------------------------------------------------------------------------------

\newcommand{\memotitle}[1]{\renewcommand{\memotitle}{#1}}
\newcommand{\memodate}[1]{\renewcommand{\memodate}{#1}}

\newcommand{\memoinfotable}[1]{\renewcommand{\memoinfotable}{#1}}

\newcommand{\leftcontactinfo}[1]{\renewcommand{\leftcontactinfo}{#1}}
\newcommand{\centercontactinfo}[1]{\renewcommand{\centercontactinfo}{#1}}
\newcommand{\rightcontactinfo}[1]{\renewcommand{\rightcontactinfo}{#1}}
