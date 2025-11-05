const Navigation = ({ currentStory, allStoryLinks, changeStory }) => {
  return (
    <div className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex overflow-x-auto">
          {allStoryLinks.map((story, index) => (
            <button
              key={index}
              onClick={() => changeStory(index)}
              className={`px-6 py-4 text-sm font-medium whitespace-nowrap border-b-2 transition-colors ${
                currentStory === index
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300'
              }`}
            >
              <div className="text-left">
                <div className="font-bold">{story.name.split(':')[1]}</div>
                <div className="text-xs text-gray-500 mt-1">{story.tagline}</div>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
